import pandas as pd


def get_unique_timeslots(df_programme: pd.DataFrame) -> list[str]:
    # We do not want to filter the timeslots, so we can just return the unique values
    return df_programme["Schedule"].unique().tolist()
