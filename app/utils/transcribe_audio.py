import requests

def transcribe_audio(audio_file, WHISPER_API_KEY):
    # Upload audio file to Whisper API
    headers = {
        "Authorization": f"Bearer {WHISPER_API_KEY}",
        "Transfer-Encoding": "chunked",
    }
    response = requests.post(
        "https://api.openai.com/v1/speech-to-text/transcriptions",
        headers=headers,
        data=audio_file.name,
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
