from .mongo import MongoSingleton


def get_distinct_channels(guild_id: str) -> list[str]:
    client = MongoSingleton.get_instance().client
    channels = client[guild_id]["rawinfos"].distinct("channelId")
    return channels
