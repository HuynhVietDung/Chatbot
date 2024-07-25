from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import logging
import streamlit as st
import pandas as pd
import json
import os
import requests
from PIL import Image
from io import BytesIO
import numpy as np

scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

def get_sheet(sheetname: str):
    # Load the credentials
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    # Authorize the client
    client = gspread.authorize(creds)

    spreadsheet = client.open(sheetname)
    sheet = spreadsheet.worksheets()[0]
    return sheet

def get_data(sheetname: str) -> pd.DataFrame:
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials2.json", scope)

    # Authorize the client
    client = gspread.authorize(creds)
    spreadsheet = client.open(sheetname)
    sheet = spreadsheet.worksheets()[0]
    # Get all values from the worksheet
    data = sheet.get_all_values()
    
    df = pd.DataFrame(data[1:], columns=data[0])

    fpath = sheetname+".csv"
    if os.path.exists(fpath):
        os.remove(fpath)
    
    df.to_csv(fpath, index= False)
    # Convert to DataFrame
    return pd.read_csv(fpath)
    
@st.cache_data
def create_credentials():
    if not os.path.isfile("credentials.json"):
        data = {
            "type": st.secrets["credentials1"]["type"],
            "project_id": st.secrets["credentials1"]["project_id"],
            "private_key_id": st.secrets["credentials1"]["private_key_id"],
            "private_key": st.secrets["credentials1"]["private_key"],
            "client_email": st.secrets["credentials1"]["client_email"],
            "client_id": st.secrets["credentials1"]["client_id"],
            "auth_uri": st.secrets["credentials1"]["auth_uri"],
            "token_uri": st.secrets["credentials1"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["credentials1"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["credentials1"]["client_x509_cert_url"],
            "universe_domain": st.secrets["credentials1"]["universe_domain"],
        }

        with open("credentials.json", "w") as file:
            json.dump(data, file)

    if not os.path.isfile("credentials2.json"):
        data2 = {
            "type": st.secrets["credentials2"]["type"],
            "project_id": st.secrets["credentials2"]["project_id"],
            "private_key_id": st.secrets["credentials2"]["private_key_id"],
            "private_key": st.secrets["credentials2"]["private_key"],
            "client_email": st.secrets["credentials2"]["client_email"],
            "client_id": st.secrets["credentials2"]["client_id"],
            "auth_uri": st.secrets["credentials2"]["auth_uri"],
            "token_uri": st.secrets["credentials2"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["credentials2"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["credentials2"]["client_x509_cert_url"],
            "universe_domain": st.secrets["credentials2"]["universe_domain"],
        }

        with open("credentials2.json", "w") as file:
            json.dump(data2, file)


def upload_image(file_path, file_name, mime_type, type="bill"):

    """Insert new file to Google Drive.

    Args:
        file_path (str): The path to the file to be uploaded.
        file_name (str): The name to be given to the file on Google Drive.
        mime_type (str): The MIME type of the file.

    Returns:
        str: The ID of the uploaded file.
    """
    scope = [
        'https://www.googleapis.com/auth/drive.file',
    ]

    # Load the credentials
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    try:
        # Create Drive API client
        service = build("drive", "v3", credentials=creds)

        file_metadata = {"name": file_name, "parents": ["1_7khZLb0MNVydXasSZsKRzbsPzgoyBua"] if type == "bill" else ["1L74LBwba5afBJF6TyQRcR0EZ3XE6Rnth"]}
        media = MediaFileUpload(file_path, mimetype=mime_type)
        
        # Upload file
        file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        logging.info(f'File ID: {file.get("id")}, Web View Link: {file.get("webViewLink")}')
        return file.get("id"), file.get("webViewLink")

    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return None

def get_image(url: str):
    # Fetch the image
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = np.array(img)
    return img
