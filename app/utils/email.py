import smtplib
import sys
import os

# Add the parent directory of the current file to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

WHISPER_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
SPREADSHEET_ID  = os.environ.get("SPREADSHEET_ID")
sheet_range = os.environ.get("sheet_range")

# from app.models.annotation import annotate_text


def generate_pitch_review(transcript):
    # annotation = annotate_text(transcript)

    review = f"""
    Pitch Review:

    Attributes:
    # annotation here

    Suggestions:
    # saved openai response here
    """

    return review


def send_email(subject, body, to):
    message = f"Subject: {subject}\n\n{body}"
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to, message)


# Usage example
# transcript = "Sample transcript text here"
# pitch_review = generate_pitch_review(transcript)
# send_email("Pitch Review", pitch_review, "sankalpthakur.avi@gmail.com")
