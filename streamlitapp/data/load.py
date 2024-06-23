import ast
import pandas as pd
import streamlit as st


# Data caching will make the app more stable and performant
@st.cache_data
def load_and_prepare_programme_data(filepath: str) -> pd.DataFrame:
    list_typed_columns = ["all_keyword_ids", "authors", "keywords"]
    date_typed_columns = ["date"]

    expected_column_types = {
        "timeslot": int,
        "schedule": str,
        "start_time": str,
        "end_time": str,
        "stream": int,
        "stream_name": str,
        "track_code": str,
        "session": int,
        "session_name": str,
        "paper_id": int,
        "title": str,
        "abstract": str,
    }
    expected_columns = list(expected_column_types.keys()) + list_typed_columns + date_typed_columns

    df_programme = pd.read_csv(
        filepath,
        usecols=expected_columns,
        dtype=expected_column_types,
        converters={col: ast.literal_eval for col in list_typed_columns},
        parse_dates=date_typed_columns
    )
    df_programme.sort_values(by=["timeslot", "stream", "session"], inplace=True)

    # Data and timestamp transformation
    df_programme["start_timedelta"] = pd.to_timedelta(df_programme["start_time"] + ':00')
    df_programme["end_timedelta"] = pd.to_timedelta(df_programme["end_time"] + ':00')

    df_programme["start_timestamp"] = df_programme["start_timedelta"] + df_programme["date"]
    df_programme["end_timestamp"] = df_programme["end_timedelta"] + df_programme["date"]

    del df_programme["start_timedelta"]
    del df_programme["end_timedelta"]

    # Rename columns for better readability
    col_name_mapping = {
        col_name: col_name.replace("_", " ").title()
        for col_name in expected_columns
    }
    df_programme.rename(columns=col_name_mapping, inplace=True)

    return df_programme
