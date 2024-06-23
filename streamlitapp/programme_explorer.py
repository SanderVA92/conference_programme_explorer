import pandas as pd
import streamlit as st
import streamlit.elements.lib.event_utils as st_event_utils
import data.load as data_loader
import data.filter as data_filter
import data.utils as data_utils
from config import AppConfig
from optimizer.max_session_utility import MaximizeSessionAttendanceUtility

st.set_page_config(layout="wide")


def display_multiselect_filters(df_programme: pd.DataFrame) -> None:
    col_multiselect_filters = st.columns(3)

    # Add a timeslot filter to the page itself
    potential_timeslots = data_utils.get_unique_timeslots(df_programme)
    col_multiselect_filters[0].multiselect("Timeslot(s)", potential_timeslots, key="selected_timeslots")

    # Add a stream filter to the page itself, in the column next to the timeslot filter
    potential_streams = data_utils.get_unique_streams(df_programme, filter_by_state=True)
    preset_streams = data_utils.get_preselected_streams(potential_streams)
    col_multiselect_filters[1].multiselect("Stream(s)", potential_streams, key="selected_streams", default=preset_streams)

    # Add a keywords filter to the page itself
    potential_keywords = data_utils.get_unique_keywords(df_programme)
    col_multiselect_filters[2].multiselect("Keyword(s)", potential_keywords, key="selected_keywords")


def display_text_based_filters() -> None:
    col_text_filters = st.columns(2)

    col_text_filters[0].text_input("Search in title ...", key="title_search")
    col_text_filters[1].text_input("Search in abstract ...", key="abstract_search")


def display_optimization_model_filters(df_programme: pd.DataFrame) -> None:
    col_optimization_filters = st.columns(2)

    all_streams = data_utils.get_unique_streams(df_programme, filter_by_state=False)

    col_optimization_filters[0].multiselect("Restrict to streams", options=all_streams, key="opt_selected_stream")

    all_sessions = data_utils.get_unique_sessions_for_optimization_model(df_programme)
    col_optimization_filters[1].multiselect("Must-attend Sessions", all_sessions, key="must_attend_sessions")


def display_all_selected_abstracts(df_programme: pd.DataFrame, selection_events: st_event_utils.AttributeDictionary) -> None:
    selected_rows = selection_events['rows']

    if len(selected_rows) == 0:
        st.info("No abstracts selected to display. Please select in the table above.")
        return

    st.write(f'Selected {len(selected_rows)} talks in the programme')

    limit = AppConfig.ABSTRACT_DISPLAY_LIMIT
    if len(selected_rows) > limit:
        st.error(
            f"Too many abstracts to display. Please refine your selection to at most {limit} abstracts."
        )
        return

    df_selected_abstracts = df_programme.iloc[selected_rows]

    for index, record in df_selected_abstracts.iterrows():
        title = f"{record['Schedule']}\t-\t {record['Title']}\t({record['Track Code']})"
        expander = st.expander(title, expanded=False)
        expander.write(record["Abstract"])

    return


def conference_browsing_tab(df_complete_programme: pd.DataFrame, **kwargs) -> None:
    container = kwargs.get('container', st)

    with container:
        display_multiselect_filters(df_complete_programme)
        display_text_based_filters()

        # Before the programme can be displayed, we need to filter it based on the user's selection, using the session state
        df_filtered = data_filter.filter_programme_based_on_state(df_complete_programme)

        # Users should be able to select rows in the dataframe to display the requested abstracts. To do so at a later
        # point, we need to capture the selection events. The on_select="rerun" setting will enable selections.
        programme_table_events = st.dataframe(
            df_filtered,
            column_order=['Schedule', 'Track Code', 'Session Name', 'Title', 'Keywords'],
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

        df_selected_sessions = get_optimal_set_of_sessions(df_available_programme)
        st.dataframe(
            df_selected_sessions,
            column_order=["Schedule", "Stream Name", "Track Code", "Session Name", "Title"],
            hide_index=True
        )


def main() -> None:
    filepath_programme = AppConfig.FILEPATH_CONFERENCE_PROGRAMME
    df_complete_programme = data_loader.load_and_prepare_programme_data(filepath_programme)
    df_complete_programme = data_utils.assign_random_utilities_to_programme_entries(df_complete_programme)

    main_page_tabs = st.tabs(['Browse Conference Programme', 'Optimize Your Schedule'])

    conference_browsing_tab(df_complete_programme, container=main_page_tabs[0])
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
