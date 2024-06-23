import pandas as pd
import streamlit as st


def get_unique_timeslots(df_programme: pd.DataFrame) -> list[str]:
    # We do not want to filter the timeslots, so we can just return the unique values
    return df_programme["Schedule"].unique().tolist()


def get_unique_streams(df_programme: pd.DataFrame, filter_by_state: bool) -> list[str]:
    # For getting the streams, we want to limit ourselves to only those which are being organized
    # during the selected timeslots - if any were selected. This leads to some kind of hierarchical filtering
    if filter_by_state is False:
        unique_streams = df_programme["Stream Name"].unique().tolist()
        unique_streams.sort()
        return unique_streams

    df_filtered = df_programme.copy()
    # Ensure that the filters are applied. We can extract the filters from the session state
    flt_timeslots = st.session_state.get("selected_timeslots", [])
    if len(flt_timeslots) > 0:
        df_filtered = df_filtered[df_filtered["Schedule"].isin(flt_timeslots)]

    unique_streams = df_filtered["Stream Name"].unique().tolist()
    unique_streams.sort()
    return unique_streams
