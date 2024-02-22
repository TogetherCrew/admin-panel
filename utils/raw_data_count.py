from datetime import datetime

from utils.mongo import MongoSingleton


def get_guild_raw_data_count(guild_id: str, from_date: datetime):
    client = MongoSingleton.get_instance().client

    raw_data_count = client[guild_id]["rawinfos"].count_documents(
        {"createdDate": {"$gte": from_date}}
    )
    return raw_data_count
