from __future__ import annotations

from typing import Any

import pandas as pd
import pulp


class MaximizeSessionAttendanceUtility:
    __dict_session_details: dict[str, dict[str, Any]]
    __opt_model: pulp.LpProblem

    __dict_session_attendance_variables: dict[str, pulp.LpBinary] = {}

    __at_most_one_session_per_slot_constraints: list[pulp.LpConstraint] = []

    def __init__(self, dict_sessions: dict[str, dict[str, Any]]) -> None:
        self.__dict_session_details = dict_sessions
        self.__opt_model = pulp.LpProblem(
            "Maximize Overall Session Attendance Utility", sense=pulp.LpMaximize
        )

    @classmethod
    def create_base_session_level_model(
        cls, df_potential_talks: pd.DataFrame
    ) -> MaximizeSessionAttendanceUtility:
        df_session_level_utility = cls.__compute_session_utility(df_potential_talks)
        dict_sessions = df_session_level_utility.to_dict(orient="index")

        model = cls(dict_sessions)

        model.__create_session_attendance_variables()

        model.__create_constraints_at_most_one_session_per_timeslot()
        model.__add_constraints_to_model(model.__at_most_one_session_per_slot_constraints)

        model.__set_objective_to_maximize_utility()

        return model

    def solve(self) -> None:
        self.__opt_model.solve(pulp.PULP_CBC_CMD(timeLimit=60, msg=False))

    def is_optimal(self) -> bool:
        return self.__opt_model.status == pulp.LpStatusOptimal

    def is_infeasible(self) -> bool:
        return self.__opt_model.status == pulp.LpStatusInfeasible

    def get_optimal_session_attendance(self) -> list[dict[str, Any]]:
        if self.is_optimal() is False:
            raise Exception(
                f"Cannot retrieve results for model with status {self.__opt_model.status}"
            )

        sessions_to_attend = []
        for session_id, session_details in self.__dict_session_details.items():
            session_variable = self.__dict_session_attendance_variables[session_id]
            if session_variable.value() < 0.99:
                continue

            session_details = self.__dict_session_details[session_id]
            sessions_to_attend.append(session_details)

        return sessions_to_attend

    def __create_session_attendance_variables(self) -> None:
        for session_id in self.__dict_session_details.keys():
            variable_name = f"session_{session_id}_attendance"

            new_variable = pulp.LpVariable(variable_name, cat=pulp.LpBinary)
            self.__dict_session_attendance_variables[session_id] = new_variable

    def __create_constraints_at_most_one_session_per_timeslot(self) -> None:
        dict_timeslot_sessions = {}
        for session_id, session_details in self.__dict_session_details.items():
            timeslot = session_details["Schedule"].strip(" ")

            if timeslot not in dict_timeslot_sessions:
                dict_timeslot_sessions[timeslot] = []

            session_variable = self.__dict_session_attendance_variables[session_id]
            dict_timeslot_sessions[timeslot].append(session_variable)

        all_constraints = []
        for timeslot, session_variables in dict_timeslot_sessions.items():
            name = f"at_most_one_session_in_timeslot_{timeslot}"
            timeslot_constraint = pulp.LpConstraint(
                pulp.lpSum(session_variables),
                rhs=1,
                sense=pulp.LpConstraintLE,
                name=name,
            )

            all_constraints.append(timeslot_constraint)

        self.__at_most_one_session_per_slot_constraints = all_constraints

    def __set_objective_to_maximize_utility(self) -> None:
        obj_function_elements = []

        for session_id, session_details in self.__dict_session_details.items():
            session_variable = self.__dict_session_attendance_variables[session_id]
            obj_function_elements.append(session_variable * session_details["Utility"])

        objective = pulp.lpSum(obj_function_elements)
        self.__opt_model.setObjective(objective)

    @staticmethod
    def __compute_session_utility(df_potential_talks: pd.DataFrame) -> pd.DataFrame:
        session_level_columns = [
            "Session Name",
            "Session",
            "Stream Name",
            "Track Code",
            "Stream",
            "Timeslot",
            "Schedule",
        ]
        utility_column = "Utility"

        columns_to_keep = session_level_columns + [utility_column]
        missing_columns = set(columns_to_keep).difference(df_potential_talks.columns)
        if len(missing_columns) > 0:
            missing_columns_str = ", ".join(missing_columns)
            raise KeyError(f"Missing columns {missing_columns_str} in DataFrame")

        df_session_level_utility = (
            df_potential_talks[columns_to_keep].groupby(by=session_level_columns).mean()
        )
        df_session_level_utility.reset_index(inplace=True)
        df_session_level_utility.set_index("Session", inplace=True)
        return df_session_level_utility

    def __add_constraints_to_model(
        self, all_constraints: list[pulp.LpConstraint]
    ) -> None:
        for constraint in all_constraints:
            self.__opt_model.addConstraint(constraint, constraint.name)
