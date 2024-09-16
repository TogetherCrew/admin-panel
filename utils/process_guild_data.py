from datetime import datetime, timedelta

from utils.mongo_utils import MongoUtils


def process_guild_data(
    platform_document: dict,
) -> dict[str, str | int | datetime | None]:
    """
    process each platform and prepare the analytics for it
    """
    platform_id = str(platform_document["_id"])
    guild_id = platform_document["metadata"]["id"]
    utils = MongoUtils(guild_id)

    guild_name = platform_document["metadata"]["name"]
    connected_at = platform_document["connectedAt"]
    disconnected_at = platform_document["disconnectedAt"]
    if "selectedChannels" in platform_document["metadata"]:
        selected_channel_count = len(platform_document["metadata"]["selectedChannels"])
    else:
        selected_channel_count = -1

    # getting the latest dates
    raw_infos_date = utils.get_latest_discord_raw_info_date()
    # fired_sage_date = utils.get_latest_fired_saga(platform_id=platform_id)
    heatmaps_date = utils.get_latest_heatmaps_date()
    memberactivities_date = utils.get_latest_memberactivities_date()
    extracted_channels = utils.get_distinct_channels()

    guild_members_count = utils.get_guild_members_count()
    # 30 days before
    raw_data_count = utils.get_raw_data_count(
        from_date=datetime.now() - timedelta(days=31)
    )

    data: dict[str, str | int | datetime | None] = {
        "guild_id": guild_id,
        "guild_name": guild_name,
        "connected_at": connected_at,
        "platform_id": platform_id,
        "disconnected_at": disconnected_at,
        "selected_channels_count": selected_channel_count,
        "extracted_channel_counts": len(extracted_channels),
        "latest_raw_info": raw_infos_date,
        # "latest_analyzer_run_fired_saga": fired_sage_date,
        "latest_heatmaps": heatmaps_date,
        "latest_memberactivities": memberactivities_date,
        "raw_data_count_30days": raw_data_count,
        "guild_members_count": guild_members_count,
    }

    return data
