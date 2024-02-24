from datetime import datetime
from typing import Any

from utils.mongo import MongoSingleton


class MongoBase:
    def __init__(self, guild_id: str) -> None:
        self.guild_id = guild_id

    def get_guild_raw_data_count(self, from_date: datetime):
        client = MongoSingleton.get_instance().client

        raw_data_count = client[self.guild_id]["rawinfos"].count_documents(
            {"createdDate": {"$gte": from_date}}
        )
        return raw_data_count

    def get_guild_members_count(self) -> int:
        client = MongoSingleton.get_instance().client
        doc_count = client[self.guild_id]["guildmembers"].count_documents({})
        return doc_count

    def get_latest_document(
        self, db_name: str, collection_name: str, date_field: str, **kwargs
    ) -> dict[str, Any]:

        filters = kwargs.get("filters", None)
        client = MongoSingleton.get_instance().client
        if filters is None:
            latest_document = client[db_name][collection_name].find_one(
                {}, sort=[(date_field, -1)]
            )
        else:
            latest_document = client[db_name][collection_name].find_one(
                filters, sort=[(date_field, -1)]
            )
        return latest_document

    def get_distinct_channels(self) -> list[str]:
        client = MongoSingleton.get_instance().client
        channels = client[self.guild_id]["rawinfos"].distinct("channelId")
        return channels

    def get_guild_platform_id(self) -> str:
        """
        get the guild platform id using the given guild id

        Returns
        --------
        platform_id : str
            the platform id related to the given guild
        """
        mongo_client = MongoSingleton.get_instance().client

        guild_info = mongo_client["Core"]["platforms"].find_one(
            {"metadata.id": self.guild_id}, {"_id": 1}
        )
        if guild_info is not None:
            platform_id = str(guild_info["_id"])
        else:
            raise ValueError(f"No available guild with id {self.guild_id}")

        return platform_id
