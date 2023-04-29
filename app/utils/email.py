import openai
import streamlit as st
import smtplib

from config import OPENAI_API_KEY, EMAIL_ADDRESS, EMAIL_PASSWORD

openai.api_key = OPENAI_API_KEY


def send_email(subject, body, to):
    message = f"Subject: {subject}\n\n{body}"
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to, message)
