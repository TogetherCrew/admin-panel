import streamlit as st
from load_data import load_mongodb_analytics
import logging


@st.cache_data
def load_data():
    mybar = st.progress(0, text="Guild Analytics Extraction Running")

    data = load_mongodb_analytics(_progress_bar=mybar)
    return data


logging.basicConfig(level=logging.INFO)

data_load_state = st.text("Loading data...")
data = load_data()
data_load_state.text("Loading data...done!")
st.subheader("MongoDB data Analytics")
st.dataframe(data, use_container_width=True, hide_index=True)
