import logging
from datetime import datetime

import pandas as pd
import streamlit as st
import yaml
from streamlit_authenticator import Authenticate
from utils.mongo import MongoSingleton
from utils.process_guild_data import process_guild_data
from yaml.loader import SafeLoader


def load_guilds_latest_date_df():
    client = MongoSingleton.get_instance().client

    cursor = client["Core"]["platforms"].find({"name": "discord"})
    guild_documents = list(cursor)

    guilds_data: list[dict[str, str | datetime]] = []

    mybar = st.progress(0, text="Guild Analytics Extraction Running")
    dataframe_widget = st.dataframe()

    for idx, guild_doc in enumerate(guild_documents):
        guild_id = guild_doc["metadata"]["id"]
        message = f"Analyzing {idx + 1}/{len(guild_documents)} guild_id: {guild_id}"
        logging.info(message)

        mybar.progress((idx + 1) / len(guild_documents), message)
        data = process_guild_data(guild_doc)

        # TODO: bring the neo4j analytics too
        guilds_data.append(data)

        df = pd.DataFrame(guilds_data)
        dataframe_widget.dataframe(df)


logging.basicConfig(level=logging.INFO)
st.subheader("TogetherCrew's Amin Panel")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"],
)
name, authentication_status, username = authenticator.login()

if authentication_status:
    authenticator.logout("Logout", "main")
    st.write(f"Welcome *{name}*")
    # st.title('Some content')
    load_guilds_latest_date_df()
elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
