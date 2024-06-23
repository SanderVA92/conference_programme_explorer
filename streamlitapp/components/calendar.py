import pandas as pd
import streamlit as st
import streamlit_calendar as st_cal

"""
This module contains the calendar component for the Streamlit app which has been built on top of the FullCalender library
originally implemented for JavaScript. The calendar component has been developed by GitHub user im-perativa and was
published on pypi: https://pypi.org/project/streamlit-calendar/
"""


def available_calendar_views() -> dict[str, str]:
    return {"Week": "timeGridWeek", "List": "list"}


def default_calendar_options(calendar_view: str):
    general_options = {
        "editable": "true",
        "navLinks": "true",
        "selectable": "true",
        "resources": [],
        # Control the limitations on the calendar browsing and display
        "slotMinTime": "08:00:00",
        "slotMaxTime": "19:00:00",
        "validRange": {
            "start": "2024-07-01",
            "end": "2024-07-04",
        },
        "initialView": calendar_view,
    }

    header_toolbar_config = {
        "right": "today prev,next",
        "center": "",
    }

    list_view_config = {
        "slotLabelFormat": [
            {"hour": "2-digit", "minute": "2-digit", "hour12": False},
        ],
        "allDaySlot": "false",
        "eventTimeFormat": {
            "hour": "2-digit",
            "minute": "2-digit",
            "hour12": False,
        }
    }
    time_grid_week_view_config = {
        "duration": {"days": 4},
        "slotLabelFormat": [
            {"hour": "2-digit", "minute": "2-digit", "hour12": False},
        ],
        "allDaySlot": "false",
        "eventTimeFormat": {
            "hour": "2-digit",
            "minute": "2-digit",
            "hour12": False,
        },
        "visibleRange": {  # Disable if looking at only the visible week
            "start": "2024-06-30",
            "end": "2024-07-04",
        },
    }

    all_options = {
        **general_options,
        "headerToolbar": header_toolbar_config,
        "views": {
            "list": list_view_config,
            "timeGridWeek": time_grid_week_view_config,
        }
    }
    return all_options


def generate_events_for_calendar(events: pd.DataFrame, must_attend_sessions: list[str]):
    events_list = []

    for index, event in events.iterrows():
        color = "blue"
        if event["Session Name"] in must_attend_sessions:
            color = "red"

        start_ts = event['Start Timestamp']
        end_ts = event['End Timestamp']

        event_dict = {
            "allDay": False,
            "title": f"{event['Session Name']}",
            "start": str(start_ts),
            "end": str(end_ts),
            "color": color,
        }
        events_list.append(event_dict)

    return events_list


def render_calendar_from_sessions(df_selected_sessions: pd.DataFrame) -> None:
    must_attend_sessions = st.session_state.get('must_attend_sessions', [])

    dict_available_calendar_views = available_calendar_views()
    calendar_view_name = st.session_state.get('calendar_view', list(dict_available_calendar_views.keys())[0])
    calendar_view_value = dict_available_calendar_views[calendar_view_name]

    all_events = generate_events_for_calendar(df_selected_sessions, must_attend_sessions)
    options = default_calendar_options(calendar_view_value)
    _ = st_cal.calendar(events=all_events, options=options)
