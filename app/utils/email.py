import smtplib
import base_nlp

from config import EMAIL_ADDRESS, EMAIL_PASSWORD


def generate_pitch_review(transcript):
    lang_code = base_nlp.detect_language(transcript)
    entities = base_nlp.named_entity_recognition(transcript, lang_code)
    sentiment = base_nlp.sentiment_analysis(transcript, lang_code)
    speakers = base_nlp.speaker_analysis(transcript, lang_code)
    keywords = base_nlp.keyword_usage(transcript, lang_code)
    objections = base_nlp.objection_handling(transcript, lang_code)

    review = f"""
    Pitch Review:

    Named Entities:
    {entities}

    Sentiment Analysis:
    {'Positive' if sentiment > 0 else 'Negative' if sentiment < 0 else 'Neutral'}

    Speaker Analysis:
    {speakers}

    Keyword Usage:
    {keywords}

    Objection Handling:
    {objections} objections found
    """

    return review


def send_email(subject, body, to):
    message = f"Subject: {subject}\n\n{body}"
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to, message)


# Usage example
transcript = "Sample transcript text here"
pitch_review = generate_pitch_review(transcript)
send_email("Pitch Review", pitch_review, "recipient@example.com")
