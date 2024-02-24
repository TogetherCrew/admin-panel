from datetime import datetime
from utils.mongo_base import MongoBase


class MongoUtils(MongoBase):
    def __init__(self, guild_id: str) -> None:
        super().__init__(guild_id)

    def get_latest_discord_raw_info_date(self) -> datetime:
        date_field = "createdDate"
        latest_document = self.get_latest_document(
            db_name=self.guild_id, collection_name="rawinfos", date_field=date_field
        )
        return self.get_latest_date(latest_document, date_field)

    def get_latest_memberactivities_date(self) -> str:
        date_field = "date"
        latest_document = self.get_latest_document(
            db_name=self.guild_id,
            collection_name="memberactivities",
            date_field=date_field,
        )
        return self.get_latest_date(latest_document, date_field)

    def get_latest_heatmaps_date(self) -> str:
        date_field = "date"
        latest_document = self.get_latest_document(
            db_name=self.guild_id, collection_name="heatmaps", date_field=date_field
        )
        return self.get_latest_date(latest_document, date_field)

    def get_latest_fired_saga(
        self, guild_id: str | None = None, platform_id: str | None = None
    ) -> datetime:
        date_field = "createdAt"
        if platform_id:
            latest_document = self.get_latest_document(
                db_name="Saga",
                collection_name="sagas",
                date_field=date_field,
                filters={
                    "data.platformId": platform_id,
                    "choreography.name": "DISCORD_SCHEDULED_JOB",
                },
            )
        elif guild_id:
            fetched_platform_id = self.get_guild_platform_id(guild_id)
            latest_document = self.get_latest_document(
                db_name="Saga",
                collection_name="sagas",
                date_field=date_field,
                filters={
                    "data.platformId": fetched_platform_id,
                    "choreography.name": "DISCORD_SCHEDULED_JOB",
                },
            )
        else:
            raise ValueError("One of guild_id or platform_id should be given")

        return self.get_latest_date(latest_document, date_field)

    def get_latest_date(self, document: dict, date_field: str) -> datetime | None:
        latest_date: datetime | None
        if document:
            latest_date = document.get(date_field, "No date field")
        else:
            latest_date = None

        return latest_date
