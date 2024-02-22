from datetime import datetime
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import pandas as pd
import streamlit as st
import logging

from utils.mongo import MongoSingleton
from utils.load_guilds_latest_dates import process_guild_data


def load_guilds_latest_date_df() -> list[dict[str, str | datetime]]:
    client = MongoSingleton.get_instance().client

    cursor = client["Core"]["platforms"].find({"name": "discord"})
    guild_documents = list(cursor)

    guilds_data: list[dict[str, str | datetime]] = []

    mybar = st.progress(0, text="Guild Analytics Extraction Running")
    dataframe_widget = st.dataframe()

    for idx, guild_doc in enumerate(guild_documents):
        guild_id = guild_doc["metadata"]["id"]
        message = f"Analyzing {idx + 1}/{len(guild_documents)} guild_id: {guild_id}"
        logging.info(message)

        mybar.progress((idx + 1) / len(guild_documents), message)
        data = process_guild_data(guild_doc)

        # TODO: bring the neo4j analytics too
        guilds_data.append(data)

        df = pd.DataFrame(guilds_data)
        dataframe_widget.dataframe(df)

    return df


def process_df(data: pd.DataFrame) -> pd.DataFrame:
    """
    add the filtering option to the dataframe
    """
    modify = st.checkbox("Add filters")
    if not modify:
        df = data.copy()
    else:
        df = data.copy()

        # Try to convert datetimes into a standard format (datetime, no timezone)
        for col in df.columns:
            if is_object_dtype(df[col]):
                try:
                    df[col] = pd.to_datetime(df[col])
                except Exception:
                    pass

            if is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.tz_localize(None)

        modification_container = st.container()

        with modification_container:
            to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
            for column in to_filter_columns:
                left, right = st.columns((1, 20))
                # Treat columns with < 10 unique values as categorical
                if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                    user_cat_input = right.multiselect(
                        f"Values for {column}",
                        df[column].unique(),
                        default=list(df[column].unique()),
                    )
                    df = df[df[column].isin(user_cat_input)]
                elif is_numeric_dtype(df[column]):
                    _min = float(df[column].min())
                    _max = float(df[column].max())
                    step = (_max - _min) / 100
                    user_num_input = right.slider(
                        f"Values for {column}",
                        min_value=_min,
                        max_value=_max,
                        value=(_min, _max),
                        step=step,
                    )
                    df = df[df[column].between(*user_num_input)]
                elif is_datetime64_any_dtype(df[column]):
                    user_date_input = right.date_input(
                        f"Values for {column}",
                        value=(
                            df[column].min(),
                            df[column].max(),
                        ),
                    )
                    if len(user_date_input) == 2:
                        user_date_input = tuple(map(pd.to_datetime, user_date_input))
                        start_date, end_date = user_date_input
                        df = df.loc[df[column].between(start_date, end_date)]
                else:
                    user_text_input = right.text_input(
                        f"Substring or regex in {column}",
                    )
                    if user_text_input:
                        df = df[df[column].astype(str).str.contains(user_text_input)]


logging.basicConfig(level=logging.INFO)

st.subheader("MongoDB data Analytics")
df = load_guilds_latest_date_df()
df = process_df(df)
st.dataframe(df, use_container_width=True, hide_index=True)
