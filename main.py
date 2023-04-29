import os.path
import pickle
import requests
import json
import io
import openai
import streamlit as st
import smtplib
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Import API keys and credentials from config.py
from config import WHISPER_API_KEY, OPENAI_API_KEY, EMAIL_ADDRESS, EMAIL_PASSWORD

openai.api_key = OPENAI_API_KEY

# Set up Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
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


def transcribe_audio(audio_file):
    # Upload audio file to Whisper API
    headers = {
        "Authorization": f"Bearer {WHISPER_API_KEY}",
        "Transfer-Encoding": "chunked",
    }
    response = requests.post(
        "https://api.openai.com/v1/speech-to-text/transcriptions",
        headers=headers,
        data=audio_file.read(),
    )
    
    # Check if the response has JSON content
    if response.headers.get("Content-Type") == "application/json":
        response_json = response.json()
    else:
        response_json = {}
    
    # Log the response and status code for the file upload
    print("File upload response:", response.status_code, response_json)
    
    # If file upload is successful, get transcription results
    if response.status_code == 200:
        job_id = response_json.get("job_id")
        if job_id:
            while True:
                response = requests.get(
                    f"https://api.openai.com/v1/speech-to-text/transcriptions/{job_id}",
                    headers=headers,
                )
                
                # Check if the response has JSON content
                if response.headers.get("Content-Type") == "application/json":
                    response_json = response.json()
                else:
                    response_json = {}
                
                # Log the response and status code for the transcription results
                print("Transcription results response:", response.status_code, response_json)
                
                # Check transcription status and return transcript if complete
                if response.status_code == 200:
                    status = response_json.get("status")
                    if status == "succeeded":
                        transcript = response_json.get("text")
                        return transcript
                    else:
                        error_reason = response_json.get("error_reason", "Unknown error")
                        print(f"Transcription failed: {error_reason}")
                        break
                else:
                    error_reason = response_json.get("error_reason", "Unknown error")
                    print("Full response content:", response.content)  # Add this line to print the full response content
                    break
        else:
            return f"Job ID not found in the response"
    else:
        error_reason = response_json.get("error_reason", "Unknown error")
        return f"File upload failed: {error_reason}"


def openai_response(prompt):
    try:
        model_engine = "text-davinci-002"
        response = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=150, n=1, stop=None, temperature=0.8)
        if response.status != 200:
            return None
        return response.choices[0].text.strip()
    except Exception as e:
        print(e)
        return None

def store_data_in_google_sheets(transcript, response):
    try:
        creds = get_credentials()
        sheets_api = build('sheets', 'v4', credentials=creds)
        
        body = {
            'values': [[transcript, response]]
        }
        sheets_api.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=sheet_range,
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")

def send_email(subject, body, to):
    message = f"Subject: {subject}\n\n{body}"
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to, message)

def main():
    st.title("Pitch Training Assistant")

    # Upload audio file
    audio_file = st.file_uploader("Upload audio file", type=["wav", "mp3", "m4a"])

    if audio_file:
        with st.spinner("Transcribing audio..."):
            transcript = transcribe_audio(audio_file)

        # Print transcript on the frontend
        st.write("Transcript:")
        st.write(transcript)

        prompt = f"You are a pitch training assistant, rate the following pitch out of 10 and suggest an improvement roadmap for the pitch:\n{transcript}"

        with st.spinner("Generating response from OpenAI..."):
            response = openai_response(f"{prompt}\n{transcript}")

        st.write("OpenAI Response:")
        st.write(response)

        # Store data in Google Sheets
        store_data_in_google_sheets(transcript, response)

        # Email results
        email = st.text_input("Enter your email address to receive the results:")
        if email: 
            send_email("Pitch Training Assistant Results", f"Transcript:\n{transcript}\n\nOpenAI Response:\n{response}", email)
            st.success("Email sent successfully.")

if __name__ == "__main__":
    main()
