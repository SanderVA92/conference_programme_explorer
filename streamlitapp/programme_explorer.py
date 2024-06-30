import pandas as pd
import streamlit as st
import streamlit.elements.lib.event_utils as st_event_utils
import data.load as data_loader
import data.filter as data_filter
import data.utils as data_utils
from config import AppConfig
from optimizer.max_session_utility import MaximizeSessionAttendanceUtility, CannotRetrieveResultsException
import components.calendar as calendar

st.set_page_config(layout="wide")


def display_multiselect_filters(df_programme: pd.DataFrame) -> None:
    # col_multiselect_filters = st.columns(3)

    # Add a timeslot filter to the page itself
    potential_timeslots = data_utils.get_unique_timeslots(df_programme)
    st.multiselect("Timeslot(s)", potential_timeslots, key="selected_timeslots")

    # Add a stream filter to the page itself, in the column next to the timeslot filter
    potential_streams = data_utils.get_unique_streams(df_programme, filter_by_state=True)
    preset_streams = data_utils.get_preselected_streams(potential_streams)
    st.multiselect("Stream(s)", potential_streams, key="selected_streams", default=preset_streams)

    # Add a keywords filter to the page itself
    potential_keywords = data_utils.get_unique_keywords(df_programme)
    st.multiselect("Keyword(s)", potential_keywords, key="selected_keywords")


def display_text_based_filters() -> None:
    col_text_filters = st.columns(2)

    st.text_input("Search in title ...", key="title_search")
    st.text_input("Search in abstract ...", key="abstract_search")


def display_optimization_model_filters(df_programme: pd.DataFrame) -> None:
    col_optimization_filters = st.columns(2)

    all_streams = data_utils.get_unique_streams(df_programme, filter_by_state=False)

    col_optimization_filters[0].multiselect("Restrict to streams", options=all_streams, key="opt_selected_stream")

    all_sessions = data_utils.get_unique_sessions_for_optimization_model(df_programme)
    preselected_sessions = data_utils.get_preselected_sessions_for_optimization_model(all_sessions)
    col_optimization_filters[1].multiselect(
        "Must-attend Sessions",
        all_sessions,
        default=preselected_sessions,
        key="must_attend_sessions"
    )


def display_all_selected_abstracts(df_programme: pd.DataFrame, selection_events: st_event_utils.AttributeDictionary) -> None:
    selected_rows = selection_events['rows']
    limit = AppConfig.ABSTRACT_DISPLAY_LIMIT

    if len(selected_rows) == 0:
        st.info(f"No abstracts selected to display. Please select at most {limit} rows in the table above.")
        return

    st.write(f'Selected {len(selected_rows)} talks in the programme. Click on the title to show the abstract.')

    if len(selected_rows) > limit:
        st.error(
            f"Too many abstracts to display. Please refine your selection to at most {limit} abstracts."
        )
        return

    df_selected_abstracts = df_programme.iloc[selected_rows]

    for index, record in df_selected_abstracts.iterrows():
        title = f"{record['Schedule']}\t-\t {record['Contribution Title']}\t({record['Track Code']} - {record['Room']})"
        expander = st.expander(title, expanded=False)
        expander.markdown(f"**{record['Contribution Title']}**")
        expander.write(f"_Room {record['Room']}_")
        expander.write(record["Abstract"])

    return


def conference_browsing_tab(df_complete_programme: pd.DataFrame, **kwargs) -> None:
    container = kwargs.get('container', st)

    with container:
        # Before the programme can be displayed, we need to filter it based on the user's selection, using the session state
        df_filtered = data_filter.filter_programme_based_on_state(df_complete_programme)

        # Users should be able to select rows in the dataframe to display the requested abstracts. To do so at a later
        # point, we need to capture the selection events. The on_select="rerun" setting will enable selections.
        st.write(":arrow_down: Select rows to display the abstracts below the table.")
        programme_table_events = st.dataframe(
            df_filtered,
            column_order=['Schedule', 'Session Name', 'Contribution Title', 'Track Code', 'Keywords'],
            hide_index=True,
            on_select="rerun",
            selection_mode="multi-row",
        )

        display_all_selected_abstracts(df_filtered, programme_table_events.selection)


def get_optimal_set_of_sessions(df_programme: pd.DataFrame) -> pd.DataFrame:
    opt_model = MaximizeSessionAttendanceUtility.create_base_session_level_model(df_programme)

    # Some of the sessions we just must attend, e.g. speaking at them. Hence, add them as fixed to the model
    must_attend_sessions = st.session_state.get("must_attend_sessions", [])
    opt_model.force_session_selection(must_attend_sessions)

    opt_model.solve()

    selected_session = opt_model.get_optimal_session_attendance()
    df_selected_sessions = pd.DataFrame(selected_session).sort_values(by=["Timeslot"])
    return df_selected_sessions


def schedule_optimizer_tab(df_complete_programme: pd.DataFrame, **kwargs) -> None:
    container = kwargs.get('container', st)

    with container:
        st.info("""
            During a conference, we want to get the most out of attending different sessions. Hence,
            we will integrate an optimization model which maximizes the total utility we get from
            attending conference sessions. Note that we assume we do not want to swap rooms during
            a session, and the mean utility of a session is the combined value of all talks included
            in it.
            
            The decision then comes down to select the best possible set of sessions out of the
            available one such that we have at most one session per timeslot.
        """)

        display_optimization_model_filters(df_complete_programme)
        df_available_programme = data_filter.filter_optimization_input_based_on_state(df_complete_programme)

        columns_result_display = st.columns(2)

        try:
            df_selected_sessions = get_optimal_set_of_sessions(df_available_programme)
        except CannotRetrieveResultsException:
            st.error("Could not retrieve results likely because of a conflict in must-attend sessions")
            st.stop()

        columns_result_display[0].dataframe(
            df_selected_sessions,
            column_order=["Schedule", "Stream Name", "Track Code", "Session Name", "Title", "Utility"],
            hide_index=True
        )

        with columns_result_display[1]:
            st.radio("Select view", calendar.available_calendar_views().keys(), key="calendar_view")
            calendar.render_calendar_from_sessions(df_selected_sessions)


def main() -> None:
    filepath_programme = AppConfig.FILEPATH_CONFERENCE_PROGRAMME
    df_complete_programme = data_loader.load_and_prepare_programme_data(filepath_programme)
    df_complete_programme = data_utils.assign_random_utilities_to_programme_entries(df_complete_programme)

    all_tabs_to_show = ['Browse Conference Programme']
    if AppConfig.SHOW_OPTIMIZATION_TAB:
        all_tabs_to_show = ['Browse Conference Programme', 'Optimize Your Schedule']

    main_page_tabs = st.tabs(all_tabs_to_show)

    with st.sidebar:
        display_multiselect_filters(df_complete_programme)

        display_text_based_filters()

    conference_browsing_tab(df_complete_programme, container=main_page_tabs[0])

    if AppConfig.SHOW_OPTIMIZATION_TAB:
        schedule_optimizer_tab(df_complete_programme, container=main_page_tabs[1])


if __name__ == '__main__':
    st.title('EURO2024 Conference Programme Explorer')

    st.info(
        f'''
            Hi there, this streamlit application allows you to explore the EURO2024 conference programme. The data 
            shown here originates from an export created on {AppConfig.DATE_OF_PROGRAMME_EXPORT}. For the most 
            up-to-date programme, please visit {AppConfig.CONFERENCE_PROGRAMME_LINK}.
        '''
    )

    main()
