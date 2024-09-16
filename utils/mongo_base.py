from datetime import datetime
from typing import Any

from bson import ObjectId
from utils.mongo import MongoSingleton


class MongoBase:
    def __init__(self, platform_id: str) -> None:
        self.platform_id = platform_id

    def get_raw_data_count(self, from_date: datetime):
        client = MongoSingleton.get_instance().client

        raw_data_count = client[self.platform_id][
            "rawmemberactivities"
        ].count_documents({"date": {"$gte": from_date}})
        return raw_data_count

    def get_guild_members_count(self) -> int:
        client = MongoSingleton.get_instance().client
        doc_count = client[self.platform_id]["rawmembers"].count_documents({})
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
        channels = client[self.platform_id]["rawmemberactivities"].distinct(
            "metadata.channel_id"
        )
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
            {"_id": ObjectId(self.platform_id)}, {"_id": 1}
        )
        if guild_info is not None:
            platform_id = str(guild_info["_id"])
        else:
            raise ValueError(f"No available platform with id {self.platform_id}")

        return platform_id
