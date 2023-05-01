
# PitchPal - Pitch Training Assistant

PitchPal is an AI-driven sales performance enhancement tool designed to help sales teams improve their pitch presentations and close deals more effectively. By leveraging state-of-the-art NLP models, advanced AI technology, and powerful analytics, PitchPal offers valuable insights into various aspects of your sales pitches, such as talk-to-listen ratio, objection handling, keyword usage, and more. Empower your sales team with the tools and insights they need to optimize their sales strategies, enhance their communication skills, and drive significant growth for your business.


## Features

Transcribe audio files of pitch presentations
Perform Named Entity Recognition, Sentiment Analysis, and other NLP tasks
Generate valuable feedback and improvement suggestions using OpenAI GPT models
Store results in Google Sheets and MongoDB for further analysis
Send pitch analysis and suggestions via email
Getting Started

## Prerequisites
To use the Pitch Training Assistant, you will need:

Python 3.7 or later
Access to the following APIs and services:
Google Speech-to-Text API
Google Drive API
Google Sheets API
OpenAI API

## Installation
Clone the repository:
bash
Copy code
git clone https://github.com/sankalpsthakur/pitchpal.git
Install the required Python packages:
Copy code
pip install -r requirements.txt
Set up the necessary API keys and credentials in config.py:
makefile
Copy code
WHISPER_API_KEY = "your-whisper-api-key"
OPENAI_API_KEY = "your-openai-api-key"
EMAIL_ADDRESS = "your-email-address"
EMAIL_PASSWORD = "your-email-password"
Set up the Google API credentials by following the official guide.

## Usage
Run the application:
Copy code
streamlit run main.py
Open the web application in your browser and upload an audio file containing a pitch presentation.
The tool will transcribe the audio, perform NLP analysis, and generate feedback using OpenAI models.
View the generated insights and suggestions in the web application, and receive them via email if desired.

## Contributing

Contributions to the Pitch Training Assistant project are welcome! To contribute, please follow these steps:

Fork the repository
Create a new branch with a descriptive name (git checkout -b your-feature)
Commit your changes (git commit -m 'Add your feature')
Push the branch to your forked repository (git push origin your-feature)
Create a Pull Request
License

This project is licensed under the MIT License. See the LICENSE file for more information.

## Acknowledgments

OpenAI for providing access to their powerful GPT models
Google Cloud for their Speech-to-Text, Drive, and Sheets APIs
Hugging Face for their comprehensive library of NLP models


[working on more features and analytics from the pitch]


<img width="486" alt="image" src="https://user-images.githubusercontent.com/31366524/235303498-422b8592-f50e-479c-be74-e5167a3ca94e.png">
