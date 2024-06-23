import pandas as pd
import streamlit as st


def has_overlapping_keywords(kws_to_check: list[str], flt_kws: list[str]) -> bool:
    overlapping_keywords = set(kws_to_check).intersection(flt_kws)
    return len(overlapping_keywords) > 0


def filter_programme_based_on_state(df_programme: pd.DataFrame) -> pd.DataFrame:
    df_filtered = df_programme.copy()

    # Ensure that the filters are applied. We can extract the filters from the session state
    flt_timeslots = st.session_state.get("selected_timeslots", [])
    if len(flt_timeslots) > 0:
        df_filtered = df_filtered[df_filtered["Schedule"].isin(flt_timeslots)]

    flt_streams = st.session_state.get("selected_streams", [])
    if len(flt_streams) > 0:
        df_filtered = df_filtered[df_filtered["Stream Name"].isin(flt_streams)]

    flt_keywords = st.session_state.get("selected_keywords", [])
    if len(flt_keywords) > 0:
        # Check for overlap in the keywords
        df_filtered = df_filtered[
            df_filtered["Keywords"].apply(lambda x: has_overlapping_keywords(x, flt_keywords))
        ]

    title_text_search = st.session_state.get("title_search", '')
    if title_text_search.strip(' ') != '':
        df_filtered = df_filtered[
            df_filtered["Title"].str.contains(title_text_search, case=False)
        ]

    abstract_text_search = st.session_state.get("abstract_search", '')
    if abstract_text_search.strip(' ') != '':
        df_filtered = df_filtered[
            df_filtered["Abstract"].str.contains(abstract_text_search, case=False)
        ]

    return df_filtered
