import io
import os
import pickle
from datetime import datetime
from pymongo import MongoClient

# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request

# Import API keys and credentials from environment variables
# WHISPER_API_KEY = os.environ.get("OPENAI_API_KEY")
# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
# EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
# EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
# SPREADSHEET_ID  = os.environ.get("SPREADSHEET_ID")
# sheet_range = os.environ.get("sheet_range")

# Set up Google Drive API and Google Sheets API
# SCOPES = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive",
# ]
# SPREADSHEET_ID = "pitchpal"
# sheet_range = "Sheet1"

# MongoDB setup
MONGODB_URI = "mongodb+srv://sankalp:3WET5FcMqovY3xQx@pitchpal.ufdz6fj.mongodb.net/test?retryWrites=true&w=majority]"  # Replace this with your MongoDB connection string
client = MongoClient(MONGODB_URI)
db = client.pitchpal
pitch_data = db.pitch_data


# def get_credentials():
#     creds = None
#     if os.path.exists("token.pickle"):
#         with open("token.pickle", "rb") as token:
#             creds = pickle.load(token)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 "credentials.json", SCOPES
#             )
#             creds = flow.run_local_server(port=0)
#         with open("token.pickle", "wb") as token:
#             pickle.dump(creds, token)
#     return creds

# def save_to_google_drive(file_name, file_data, mime_type, parent_id):
#     drive_api = build("drive", "v3", credentials=get_credentials())

#     file_metadata = {
#         "name": file_name,
#         "parents": [parent_id],
#     }
#     file = drive_api.files().create(
#         body=file_metadata,
#         media_body=io.BytesIO(file_data),
#         media_mime_type=mime_type,
#         fields="id",
#     ).execute()

#     return file.get("id")

# def store_data_in_google_sheets(transcript, response, spreadsheet_id, sheet_range):
#     try:
#         sheets_api = build("sheets", "v4", credentials=get_credentials())

#         body = {
#             "values": [[transcript, response]]
#         }
#         sheets_api.spreadsheets().values().append(
#             spreadsheetId=spreadsheet_id,
#             range=sheet_range,
#             valueInputOption="RAW",
#             insertDataOption="INSERT_ROWS",
#             body=body,
#         ).execute()
#     except HttpError as error:
#         print(f"An error occurred: {error}")


# Test Google Sheets 
# store_data_in_google_sheets(
#     "sample_transcript",
#     "sample_response",
#     SPREADSHEET_ID,
#     sheet_range,
# )

def store_data_in_mongodb(user_id, audio_file_drive_id, transcript_drive_id, transcript, llm_response):
    try:
        data = {
            "user_id": user_id,
            "audio_file_drive_id": audio_file_drive_id,
            "transcript_drive_id": transcript_drive_id,
            "transcript": transcript,
            "response": llm_response,
            "timestamp": datetime.now()
        }
        pitch_data.insert_one(data)
    except Exception as error:
        print(f"An error occurred: {error}")

# Test data storage
store_data_in_mongodb(
    1,
    "sample_audio_file_drive_id",
    "sample_transcript_drive_id",
    "sample_transcript",
    "sample_response",
)
