import pandas as pd
import streamlit as st
import data.load as data_loader
import data.utils as data_utils
from config import AppConfig

st.set_page_config(layout="wide")


def filter_programme_based_on_state(df_programme: pd.DataFrame) -> pd.DataFrame:
    df_filtered = df_programme.copy()

    # Ensure that the filters are applied. We can extract the filters from the session state
    flt_timeslots = st.session_state.get("selected_timeslots", [])
    if len(flt_timeslots) > 0:
        df_filtered = df_filtered[df_filtered["Schedule"].isin(flt_timeslots)]

    flt_streams = st.session_state.get("selected_streams", [])
    if len(flt_streams) > 0:
        df_filtered = df_filtered[df_filtered["Stream Name"].isin(flt_streams)]

    return df_filtered


def main() -> None:
    filepath_programme = AppConfig.FILEPATH_CONFERENCE_PROGRAMME
    df_complete_programme = data_loader.load_and_prepare_programme_data(filepath_programme)

    col_multiselect_filters = st.columns(2)

    # Add a timeslot filter to the page itself
    potential_timeslots = data_utils.get_unique_timeslots(df_complete_programme)
    col_multiselect_filters[0].multiselect("Timeslot(s)", potential_timeslots, key="selected_timeslots")

    # Add a stream filter to the page itself, in the column next to the timeslot filter
    potential_streams = data_utils.get_unique_streams(df_complete_programme, filter_by_state=True)
    col_multiselect_filters[1].multiselect("Stream(s)", potential_streams, key="selected_streams")

    # Before the programme can be displayed, we need to filter it based on the user's selection, using the session state
    df_filtered = filter_programme_based_on_state(df_complete_programme)

    st.dataframe(
        df_filtered,
        column_order=['Schedule', 'Track Code', 'Session Name', 'Title', 'Keywords'],
        hide_index=True
    )


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
