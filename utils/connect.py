import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd
import json
import os

@st.cache_data(ttl=3)
def get_sheet(sheetname: str):
    # Define the scope
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    # Load the credentials
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    # Authorize the client
    client = gspread.authorize(creds)

    spreadsheet = client.open(sheetname)
    sheet = spreadsheet.worksheets()[0]

    return sheet

@st.cache_data(ttl=3)
def get_data(sheetname: str) -> pd.DataFrame:
    # Define the scope
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    # Load the credentials
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    # Authorize the client
    client = gspread.authorize(creds)
    spreadsheet = client.open(sheetname)

    sheet = spreadsheet.worksheets()[0]

    # Get all values from the worksheet
    data = sheet.get_all_values()

    # Convert to DataFrame
    return pd.DataFrame(data[1:], columns=data[0])

@st.cache_data
def create_credentials():
    if not os.path.isfile("credentials.json"):
        data = {
            "type": st.secrets["type"],
            "project_id": st.secrets["project_id"],
            "private_key_id": st.secrets["private_key_id"],
            "private_key": st.secrets["private_key"],
            "client_email": st.secrets["client_email"],
            "client_id": st.secrets["client_id"],
            "auth_uri": st.secrets["auth_uri"],
            "token_uri": st.secrets["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["client_x509_cert_url"],
            "universe_domain": st.secrets["universe_domain"],
        }

        with open("credentials.json", "w") as file:
            json.dump(data, file)
