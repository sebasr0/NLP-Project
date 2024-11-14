# spark_init.py
import sparknlp
import streamlit as st

@st.cache_resource
def get_spark_session():
    # Initialize Spark session only once
    return sparknlp.start()

