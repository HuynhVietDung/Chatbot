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
import time

@st.cache_data(ttl=2)
def get_sheet(sheetname: str):
    # Define the scope
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    while True:
        try:
            # Load the credentials
            creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

            # Authorize the client
            client = gspread.authorize(creds)

            spreadsheet = client.open(sheetname)
            sheet = spreadsheet.worksheets()[0]
            return sheet
        except: 
            time.sleep(10)
    

def get_all_data():
    # Define the scope
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    while True: 
        try:
            # Load the credentials
            creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

            # Authorize the client
            client = gspread.authorize(creds)
            for sh in client.openall():
                sheet = sh.worksheets()[0]
                # Get all values from the worksheet
                data = sheet.get_all_values()

                # Convert to DataFrame
                df =  pd.DataFrame(data[1:], columns=data[0])
                file_path = sh.title + ".csv"
                if os.path.exists(file_path):
                    # Remove the file
                    os.remove(file_path)
                df.to_csv(file_path, index=False)
                del df
            return
        except:
            time.sleep(10)

def get_data(sheetname: str) -> pd.DataFrame:
    file_path = sheetname + ".csv"
    if not os.path.exists(file_path):
        get_all_data()
    
    return pd.read_csv(file_path)

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
