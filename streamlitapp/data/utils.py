import random

import pandas as pd
import streamlit as st

random.seed(42)


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


def get_preselected_streams(available_streams: list[str]) -> list[str]:
    last_selected_streams = set(st.session_state.get("selected_streams", []))
    remaining_streams = set(available_streams).intersection(last_selected_streams)
    remaining_streams = list(remaining_streams)
    remaining_streams.sort()

    return remaining_streams


def get_unique_keywords(df_programme: pd.DataFrame) -> list[str]:
    # We do not want to pre-filter the keywords as there is not really a hierarchical structure
    stacked_keywords = df_programme["Keywords"].apply(pd.Series).stack()

    unique_keywords = stacked_keywords.unique().tolist()
    unique_keywords.sort()

    return unique_keywords




def get_unique_sessions_for_optimization_model(df_programme: pd.DataFrame) -> list[str]:
    df_filtered = df_programme.copy()

    # Ensure that the relevant filters are applied. We can extract the filters from the session state
    flt_streams = st.session_state.get("opt_selected_stream", [])
    if len(flt_streams) > 0:
        df_filtered = df_filtered[df_filtered["Stream Name"].isin(flt_streams)]

    unique_streams = df_filtered["Session Name"].unique().tolist()
    unique_streams.sort()
    return unique_streams


def get_preselected_sessions_for_optimization_model(available_sessions: list[str]) -> list[str]:
    last_selected_sessions = set(st.session_state.get("must_attend_sessions", []))
    remaining_sessions = set(available_sessions).intersection(last_selected_sessions)
    remaining_sessions = list(remaining_sessions)
    remaining_sessions.sort()

    return remaining_sessions


@st.cache_data
def assign_random_utilities_to_programme_entries(df_programme: pd.DataFrame) -> pd.DataFrame:
    # For illustration purposes, we will assign random utilities to the programme entries
    df_programme["Utility"] = [round(10 * random.random(), 2) for _ in range(len(df_programme))]
    return df_programme
