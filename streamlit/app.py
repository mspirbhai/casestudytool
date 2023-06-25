import streamlit as st
import requests
import json
import pandas as pd
import os
import textwrap


# Import Profiling Capability
import ydata_profiling
from streamlit_pandas_profiling import st_profile_report

# Machine Learning Tools
from pycaret.regression import setup, compare_models, pull, save_model

with st.sidebar:
    st.image("staticfiles/images/Logo.png")
    st.title("Casestudy ML App")
    choice = st.radio(
        "Navigation",
        [
            "About",
            "Data Collection",
            "Profiling",
            "Machine Learning",
            "Download",
        ],
    )
    st.info("Application to enable building ML pipeline with the casestudy data")

if os.path.exists("staticfiles/caselogs.csv"):
    df = pd.read_csv("staticfiles/caselogs.csv", index_col=None)


if choice == "About":
    st.title("About")
    st.write(
        textwrap.dedent(
            """
        This web app is an interactive web-based tool that allows users to explore a dataset, select features, and run machine learning models on them. The app is designed to be easy to use and accessible to both beginners and experienced data scientists.

        The app starts by displaying the dataset in a table format, allowing users to explore the data and get a sense of its structure and content. Users can sort and filter the data to focus on specific subsets of the data, and can also download the dataset for further analysis.

        Once users have selected the target of the dataset they want to work with, they can choose a feature to use as the target variable for machine learning. The app currently only supports regression. Users can choose the parameter to train on with the app's default settings for a quick and easy analysis.

        Once the model has been trained, the app displays the results in an easy-to-read format, including accuracy metrics of the model's performance. Users can also explore the model's predictions and see how well it predicts values for new data.

        Finally, the app allows users to download the best calculated model as a file, allowing them to save the model and use it in other applications or workflows. This feature makes it easy for users to take their work from the app and apply it to real-world problems.
        """
        )
    )
elif choice == "Data Collection":
    st.title("Data Collection - API call to get and store all Caselogs")
    refresh_button = st.button("Refresh")
    if refresh_button:
        response = requests.get("http://localhost:8000/api/caselogs")
        data = json.loads(response.text)
        df = pd.json_normalize(data)
        df.to_csv("staticfiles/caselogs.csv", index=None)
    st.info(
        "To add a row scroll to the bottom, to delete a row, select one or more rows and press delete"
    )
    st.data_editor(df, num_rows="dynamic")
elif choice == "Profiling":
    st.title("Exploratory Data Analysis on Caselogs")
    profile_report = ydata_profiling.ProfileReport(df)
    st_profile_report(profile_report, key="store")
elif choice == "Machine Learning":
    st.title("Machine Learning for Casestudy Caselogs")
    target = st.selectbox("Target", df.columns)
    go_button = st.button("Go")
    if go_button:
        df = df.dropna(subset=[target])
        setup(df, target=target, verbose=False)
        setup_df = pull()
        st.info("Find the best model for the dataset")
        st.dataframe(setup_df)
        best_model = compare_models()
        compare_df = pull()
        st.info("This is the best model found")
        st.dataframe(compare_df)
        best_model
        save_model(best_model, "best_model")
elif choice == "Download":
    st.title("Download the best model calculated")
    if os.path.exists("best_model.pkl"):
        with open("best_model.pkl", "rb") as f:
            st.download_button("Download Model", f, file_name="best_model.pkl")
    else:
        st.info("No model found")
