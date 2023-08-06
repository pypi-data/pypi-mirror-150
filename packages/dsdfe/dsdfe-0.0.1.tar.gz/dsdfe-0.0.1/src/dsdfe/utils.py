import pandas as pd

def generate_datetime_range(start: str, end: str) -> pd.DatetimeIndex:
    """Returns hourly datetime range - start inclusive, end exclusive"""
    return pd.date_range(start, end, freq="H", inclusive="left")