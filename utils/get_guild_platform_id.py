from utils.mongo import MongoSingleton


def get_guild_platform_id(guild_id: str) -> str:
    """
    get the guild platform id using the given guild id

    Parameters
    ------------
    guild_id : str
        the id for the specified guild

    Returns
    --------
    platform_id : str
        the platform id related to the given guild
    """
    mongo_client = MongoSingleton.get_instance().client

    guild_info = mongo_client["Core"]["platforms"].find_one(
        {"metadata.id": guild_id}, {"_id": 1}
    )
    if guild_info is not None:
        platform_id = str(guild_info["_id"])
    else:
        raise ValueError(f"No available guild with id {guild_id}")

    return platform_id
