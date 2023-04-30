import os.path
import pickle
import requests
import json
import io
import openai
import streamlit as st
import smtplib

# Import Google API libraries
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Import functions from other files
from app.utils.transcribe_audio import transcribe_audio
from app.utils.email import send_email
from app.utils import analytics
from app.models.annotation import detect_language, named_entity_recognition, sentiment_analysis, speaker_analysis, keyword_usage, objection_handling, annotate_text
from app.models.openai import openai_response


# Import API keys and credentials from config.py
from config import WHISPER_API_KEY, OPENAI_API_KEY, EMAIL_ADDRESS, EMAIL_PASSWORD, SPREADSHEET_ID, sheet_range

openai.api_key = OPENAI_API_KEY

import app.utils.analytics

def main():
    st.title("Pitch Training Assistant")

    # Upload audio file
    audio_file = st.file_uploader("Upload audio file", type=["wav", "mp3", "m4a"])

    if audio_file:
        with st.spinner("Transcribing audio and saving to Google Drive..."):

            st.sidebar.write("Uploading and Saving audio file...")  # Add this line
            audio_file_name = audio_file.name
            audio_file_drive_id = analytics.save_to_google_drive(audio_file_name, audio_file.read(), audio_file.content_type, "pitchpal/audio")

            st.sidebar.write("Transcribing audio...")  # Add this line
            transcript = transcribe_audio(audio_file)
            
            st.sidebar.write("Saving transcript...")  # Add this line
            transcript_drive_id = analytics.save_to_google_drive(f"{audio_file_name}_transcript.txt", transcript.encode(), "text/plain", "pitchpal/transcript")

            st.sidebar.write("Done!")  # Add this line

        # Print transcript on the frontend
        st.write("Transcript:")
        st.write(transcript)

        # Perform NLP analysis
        st.sidebar.write("Performing NLP analysis...")
        annotation = annotate_text(transcript)
        st.sidebar.write("NLP analysis completed.")

        # Prepare and send prompt to OpenAI
        system_prompt = f"You are a pitch training assistant, rate the following pitch out of 10 and suggest an improvement roadmap for the pitch:"
        
        prompt = openai_response(system_prompt + transcript + json.dumps(annotation, indent=2))

        with st.spinner("Generating response from OpenAI..."):
            response = openai_response(prompt)

        st.write("OpenAI Response:")
        st.write(response)

        # Store data in Google Sheets
        analytics.store_data_in_google_sheets(transcript, response, SPREADSHEET_ID, sheet_range)

        # Store data in MongoDB
        user_id = 1  # Replace this with the actual user ID
        analytics.store_data_in_mongodb(user_id, audio_file_drive_id, transcript_drive_id, transcript, response)

        # Email results
        email = st.text_input("Enter your email address to receive the results:")
        if email: 
            send_email("Pitch Training Assistant Results", f"Transcript:\n{transcript}\n\nOpenAI Response:\n{response}", email)
            st.success("Email sent successfully.")

if __name__ == "__main__":
    main()
