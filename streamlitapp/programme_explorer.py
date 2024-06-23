import pandas as pd
import streamlit as st
import data.load as data_loader
import data.filter as data_filter
import data.utils as data_utils
from config import AppConfig

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


def main() -> None:
    filepath_programme = AppConfig.FILEPATH_CONFERENCE_PROGRAMME
    df_complete_programme = data_loader.load_and_prepare_programme_data(filepath_programme)

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

    st.write(programme_table_events)


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
