import logging
from datetime import datetime

import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
from streamlit_authenticator import Authenticate, Hasher
from utils.mongo import MongoSingleton
from utils.process_guild_data import process_guild_data


logging.basicConfig(level=logging.INFO)
load_dotenv()
st.subheader("TogetherCrew's Amin Panel")
# Get environment variables
names = os.getenv("NAMES").split(",")
usernames = os.getenv("USERNAMES").split(",")
passwords = os.getenv("PASSWORDS").split(",")
secret_key = os.getenv("SECRET_KEY")
hashed_passwords = Hasher(passwords).generate()

# Set up the authenticator
authenticator = Authenticate(
    credentials={
        "usernames": {
            usernames[i]: {"name": names[i], "password": hashed_passwords[i]}
            for i in range(len(usernames))
        }
    },
    cookie_name="auth_cookie",
    key=secret_key,
    cookie_expiry_days=30,
)

# Login function
name, authentication_status, username = authenticator.login()

if authentication_status:
    authenticator.logout("Logout", "main")
    st.write(f"Welcome *{name}*")

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

elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
