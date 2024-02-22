from datetime import datetime, timedelta
from dateutil import parser
import pandas as pd
import logging

from utils.mongo import MongoSingleton
from utils.latest_dates import (
    get_latest_discord_raw_info_date,
    get_latest_memberactivities_date,
    get_latest_fired_saga,
    get_latest_heatmaps_date,
)
from utils.raw_data_count import get_guild_raw_data_count
import streamlit as st


def load_guilds_latest_dates(_progress_bar=None) -> list[dict[str, str | datetime]]:
    client = MongoSingleton.get_instance().client

    cursor = client["Core"]["platforms"].find({"name": "discord"})
    guild_documents = list(cursor)

    guilds_data: list[dict[str, str | datetime]] = []

    for idx, guild_doc in enumerate(guild_documents):
        guild_id = guild_doc["metadata"]["id"]
        message = f"Analyzing {idx + 1}/{len(guild_documents)} guild_id: {guild_id}"
        if _progress_bar:
            _progress_bar.progress((idx + 1) / len(guild_documents), text=message)
        logging.info(message)

        data = process_guild_data(guild_doc)
        # TODO: bring the neo4j analytics too
        guilds_data.append(data)

    if _progress_bar:
        _progress_bar.empty()

    return guilds_data


def process_guild_data(platform_document: dict) -> dict[str, str | datetime | None]:
    data: dict[str, str | datetime | None] = {}

    platform_id = str(platform_document["_id"])
    guild_id = platform_document["metadata"]["id"]
    guild_name = platform_document["metadata"]["name"]
    connected_at = platform_document["connectedAt"]
    disconnected_at = platform_document["disconnectedAt"]
    if "selectedChannels" in platform_document["metadata"]:
        selected_channel_count = len(platform_document["metadata"]["selectedChannels"])
    else:
        selected_channel_count = -1

    data["guild_id"] = guild_id
    data["guild_name"] = guild_name
    data["connected_at"] = connected_at
    data["platform_id"] = platform_id
    data["selected_channels_count"] = selected_channel_count
    data["disconnected_at"] = disconnected_at

    # getting the latest dates
    raw_infos_date = get_latest_discord_raw_info_date(guild_id)
    fired_sage_date = get_latest_fired_saga(platform_id=platform_id)
    heatmaps_date = get_latest_heatmaps_date(guild_id)
    memberactivities_date = get_latest_memberactivities_date(guild_id)
    # 30 days before
    raw_data_count = get_guild_raw_data_count(
        guild_id, from_date=datetime.now() - timedelta(days=31)
    )

    data["latest_raw_info"] = raw_infos_date
    data["latest_fired_saga"] = fired_sage_date
    data["latest_heatmaps"] = heatmaps_date
    data["latest_memberactivities"] = memberactivities_date
    data["raw_data_count_30days"] = raw_data_count

    return data


def load_guilds_analytics_pandas(_progress_bar=None) -> pd.DataFrame:
    guilds_data = load_guilds_latest_dates(_progress_bar)
    df = pd.DataFrame(guilds_data)

    df = df.sort_values(by="connected_at", ascending=False).reset_index(drop=True)
    return df
