from typing import Any

from utils.mongo import MongoSingleton


def get_latest_document(
    db_name: str, collection_name: str, date_field: str, **kwargs
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
