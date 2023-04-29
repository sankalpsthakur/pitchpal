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
from transcribe_audio import transcribe_audio
from email import send_email
from analytics import save_to_google_drive, store_data_in_google_sheets


# Import API keys and credentials from config.py
from config import WHISPER_API_KEY, OPENAI_API_KEY, EMAIL_ADDRESS, EMAIL_PASSWORD

openai.api_key = OPENAI_API_KEY



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



def main():
    st.title("Pitch Training Assistant")

    # Upload audio file
    audio_file = st.file_uploader("Upload audio file", type=["wav", "mp3", "m4a"])

    if audio_file:
        with st.spinner("Transcribing audio and saving to Google Drive..."):

            st.sidebar.write("Uploading and Saving audio file...")  # Add this line
            audio_file_name = audio_file.name
            audio_file_drive_id = save_to_google_drive(audio_file_name, audio_file.read(), audio_file.content_type, "pitchpal/audio")

            st.sidebar.write("Transcribing audio...")  # Add this line
            transcript = transcribe_audio(audio_file)
            
            st.sidebar.write("Saving transcript...")  # Add this line
            transcript_drive_id = save_to_google_drive(f"{audio_file_name}_transcript.txt", transcript.encode(), "text/plain", "pitchpal/transcript")

            st.sidebar.write("Done!")  # Add this line

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

