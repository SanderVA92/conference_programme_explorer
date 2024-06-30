import ast
import os
import streamlit as st


class AppConfig:
    ROOT_DIR: str = os.path.join(os.path.dirname(__file__), "..")
    DATASET_DIR: str = os.path.join(ROOT_DIR, "datasets")

    # FILENAME_CONFERENCE_PROGRAMME: str = "20240621_complete_EURO2024_conference_programme.csv"
    FILENAME_CONFERENCE_PROGRAMME: str = "20240621_EURO2024_conference_programme_rooms.csv"
    DATE_OF_PROGRAMME_EXPORT = "2024-06-21"
    CONFERENCE_PROGRAMME_LINK = "https://euro2024cph.dk/programme/conference-program"

    FILEPATH_CONFERENCE_PROGRAMME: str = os.path.join(DATASET_DIR, FILENAME_CONFERENCE_PROGRAMME)

    ABSTRACT_DISPLAY_LIMIT: int = 10

    __FEATURE_TOGGLES: dict[str, str] = st.secrets.get("feature_toggles", {})
    SHOW_OPTIMIZATION_TAB: bool = ast.literal_eval(__FEATURE_TOGGLES.get("show_optimization_tab", "False"))
