# Pitch Training Assistant
This repo contains code for a pitch training assistant that can transcribe audio files, rate pitches, and suggest improvement roadmaps.

# Features
Transcribe audio files
Rate pitches out of 10
Suggest improvement roadmaps for pitches

# How to use
Clone the repo to your local machine.
Install the dependencies by running the following command in the terminal:
pip install -r requirements.txt

Run the main script by running the following command in the terminal:
python main.py

pitchpal/
│
├── app/                       # Main application folder
│   ├── main.py                # Main application entry point
│   ├── config.py              # Configuration file containing API keys and other settings
│   ├── utils/                 # Utility functions and classes
│   │   ├── transcribe.py      # Functions for transcribing audio
│   │   ├── analytics.py       # Functions for generating in-depth analytics
│   │   ├── integration.py     # Functions for integrating with CRM and communication platforms
│   │   └── email.py           # Functions for sending email notifications
│   │
│   ├── dashboard/             # Dashboard related components
│   │   ├── dashboard.py       # Main dashboard component
│   │   ├── widgets.py         # Custom widgets for displaying data and metrics
│   │   └── templates/         # HTML templates for dashboard components
│   │
│   ├── api/                   # API endpoints for PitchPal
│   │   ├── __init__.py        # Initialize API endpoints
│   │   ├── transcription.py   # Transcription related API endpoints
│   │   └── analytics.py       # Analytics related API endpoints
│   │
│   └── tests/                 # Unit and integration tests
│       ├── conftest.py        # Test configuration and fixtures
│       ├── test_transcribe.py # Tests for transcription functionality
│       └── test_analytics.py  # Tests for analytics functionality
│
├── models/                    # Machine learning models and related scripts
│   ├── train.py               # Script for training ML models
│   ├── predict.py             # Script for generating predictions with trained models
│   └── evaluation.py          # Script for evaluating model performance
│
├── data/                      # Data storage and processing
│   ├── raw/                   # Raw data storage (audio files, transcripts)
│   ├── processed/             # Processed data storage (analyzed transcripts, metrics)
│   └── scripts/               # Data processing scripts
│       ├── preprocess.py      # Preprocessing raw data
│       └── aggregate.py       # Aggregating and summarizing processed data
│
├── integrations/              # Integration code for CRM and communication platforms
│   ├── crm/                   # CRM integration code
│   └── communication/         # Communication platform integration code
│
├── static/                    # Static files (CSS, JavaScript, images)
│   ├── css/                   # CSS files
│   ├── js/                    # JavaScript files
│   └── img/                   # Images
│
├── templates/                 # HTML templates
│   ├── base.html              # Base template with common layout elements
│   ├── index.html             # Homepage template
│   └── dashboard.html         # Dashboard template
│
├── docs/                      # Documentation
│   ├── user-guide.md          # User guide
│   ├── dev-guide.md           # Developer guide
│   └── api-reference.md       # API reference
│
└── .gitignore                 # Git ignore file
