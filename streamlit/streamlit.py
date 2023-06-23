import streamlit as st
import requests
import json
import pandas as pd
import os


# Import Profiling Capability
import ydata_profiling
from streamlit_pandas_profiling import st_profile_report

# Machine Learning Tools
from pycaret.regression import 

with st.sidebar:
    st.image("staticfiles/images/Logo.png")
    st.title("Casestudy ML App")
    choice = st.radio(
        "Navigation",
        [
            "Data Collection - Returning here will reset Dataframe",
            "Profiling",
            "ML",
            "Download",
        ],
    )
    st.info("Application to enable building ML pipeline with the casestudy data")

if os.path.exists("staticfiles/caselogs.csv"):
    df = pd.read_csv("staticfiles/caselogs.csv", index_col=None)

if choice == "Data Collection - Returning here will reset Dataframe":
    st.write("Data Collection")
    response = requests.get("http://localhost:8000/api/caselogs")
    data = json.loads(response.text)
    df = pd.json_normalize(data)
    df.to_csv("staticfiles/caselogs.csv", index=None)
    st.dataframe(df)
elif choice == "Profiling":
    st.title("Exploratory Data Analysis")
    profile_report = ydata_profiling.ProfileReport(df)
    st_profile_report(profile_report)
elif choice == "ML":
    st.write("ML")
elif choice == "Download":
    st.write("Download")
