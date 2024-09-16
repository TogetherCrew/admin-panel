from datetime import datetime

from utils.mongo_base import MongoBase


class MongoUtils(MongoBase):
    def __init__(self, platform_id: str) -> None:
        super().__init__(platform_id)

    def get_latest_discord_raw_info_date(self) -> datetime | None:
        date_field = "date"
        latest_document = self.get_latest_document(
            db_name=self.platform_id,
            collection_name="rawmemberactivities",
            date_field=date_field,
        )
        return self.get_latest_date(latest_document, date_field)

    def get_latest_memberactivities_date(self) -> str:
        date_field = "date"
        latest_document = self.get_latest_document(
            db_name=self.platform_id,
            collection_name="memberactivities",
            date_field=date_field,
        )
        return self.get_latest_date(latest_document, date_field)  # type: ignore

    def get_latest_heatmaps_date(self) -> str:
        date_field = "date"
        latest_document = self.get_latest_document(
            db_name=self.platform_id, collection_name="heatmaps", date_field=date_field
        )
        return self.get_latest_date(latest_document, date_field)  # type: ignore

    # def get_latest_fired_saga(
    #     self, platform_id: str | None = None
    # ) -> datetime | None:
    #     date_field = "createdAt"
    #     latest_document = self.get_latest_document(
    #         db_name="Saga",
    #         collection_name="sagas",
    #         date_field=date_field,
    #         filters={
    #             "data.platformId": platform_id,
    #             "choreography.name": "DISCORD_SCHEDULED_JOB",
    #         },
    #     )

    #     return self.get_latest_date(latest_document, date_field)

    def get_latest_date(self, document: dict, date_field: str) -> datetime | None:
        latest_date: datetime | None
        if document:
            latest_date = document.get(date_field, "No date field")
        else:
            latest_date = None

        return latest_date
