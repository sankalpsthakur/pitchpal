import os.path
import pickle
import requests
import json
import io
import openai
import streamlit as st
import smtplib
from dotenv import load_dotenv
import sys
import os

# Load environment variables from .env file
load_dotenv()

# Use the environment variable
api_key = os.environ.get('OPENAI_API_KEY')

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
from app.models.openai import openai_response

# Import API keys and credentials from environment variables
WHISPER_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
SPREADSHEET_ID  = os.environ.get("SPREADSHEET_ID")
sheet_range = os.environ.get("sheet_range")
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
            audio_file_drive_id = 1

            st.sidebar.write("Transcribing audio...")  # Add this line
            transcript = transcribe_audio(audio_file, OPENAI_API_KEY)
            
            st.sidebar.write("Saving transcript...")  # Add this line
            transcript_drive_id = 1

            st.sidebar.write("Done!")  # Add this line

        # Print transcript on the frontend
        st.write("Transcript:")
        st.write(transcript)

        system_prompt = f"You are a pitch training assistant, rate the following pitch and suggest an improvement roadmap for the pitch:"
        transcript="Hello World"
        prompt = openai_response(system_prompt + json.dumps(transcript))

        with st.spinner("Generating response from OpenAI..."):
            response = openai_response(prompt)

        st.write("Feedback on the Call Pitch:")
        st.write(response)

        # Store data in MongoDB
        user_id = 1  # Replace this with the actual user ID
        analytics.store_data_in_mongodb(user_id, audio_file_drive_id, transcript_drive_id, transcript, response)

        # Email results
        email = st.text_input("Enter your email address to receive the results:")
        if email: 
            send_email("Pitch Training Assistant Results", f"Transcript:\n{transcript}\n\nOpenAI Response:\n{response}", email)
            st.success("Email sent successfully.")

        # Collect feedback from the user
        feedback_options = ['Like', 'Dislike']
        feedback = st.radio("Do you like or dislike the AI's response?", feedback_options)
        if st.button("Submit Feedback"):
            # Store feedback in the database
            analytics.store_data_in_mongodb(user_id, audio_file_drive_id, transcript_drive_id, transcript, response, feedback)
            st.success("Feedback submitted successfully")

if __name__ == "__main__":
    main()
