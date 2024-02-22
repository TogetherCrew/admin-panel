import pandas as pd

from utils.load_guilds_latest_dates import load_guilds_analytics_pandas


def load_mongodb_analytics(_progress_bar=None) -> pd.DataFrame:
    df = load_guilds_analytics_pandas(_progress_bar)
    return df
