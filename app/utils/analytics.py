import io
import pickle
import os.path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Set up Google Drive API and Google Sheets API
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',  
]
SPREADSHEET_ID = 'pitchpal'
sheet_range = 'Sheet1'


def get_credentials():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def save_to_google_drive(file_name, file_data, mime_type, parent_id):
    drive_api = build('drive', 'v3', credentials=get_credentials())

    file_metadata = {
        'name': file_name,
        'parents': [parent_id]
    }
    file = drive_api.files().create(
        body=file_metadata,
        media_body=io.BytesIO(file_data),
        media_mime_type=mime_type,
        fields='id'
    ).execute()

    return file.get('id')

def store_data_in_google_sheets(transcript, response, spreadsheet_id, sheet_range):
    try:
        sheets_api = build('sheets', 'v4', credentials=get_credentials())

        body = {
            'values': [[transcript, response]]
        }
        sheets_api.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=sheet_range,
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")
