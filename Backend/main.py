import os
import json
import google.generativeai as genai
import google.generativeai as genai
from flask import Flask, request, jsonify
from google.cloud import speech
from pydub import AudioSegment
from werkzeug.utils import secure_filename
import google.generativeai as genai

# Load Google API Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Admin/Documents/google_credentials.json"

# Initialize Gemini API
genai.configure(api_key=AIzaSyD3yp-QXCCY-0wjUlxXE5hsSohKANjZwQ0)  # Replace with your Gemini API key

app = Flask(__name__)

def transcribe_audio(file_path):
    """Convert speech in audio file to text using Google Speech-to-Text API"""
    client = speech.SpeechClient()

    with open(file_path, "rb") as audio_file:
        audio = speech.RecognitionAudio(content=audio_file.read())

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,  # Set encoding to MP3
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)
    
    if response.results:
        transcript = response.results[0].alternatives[0].transcript
        return transcript
    return ""

def summarize_text(text):
    """Summarize the transcribed text using Google Gemini API"""
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"Summarize this text in a few sentences:\n{text}")
    return response.text.strip()

@app.route("/process_voice", methods=["POST"])
def process_voice():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    file = request.files["audio"]
    filename = secure_filename(file.filename)
    file_path = os.path.join("uploads", filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(file_path)

    # Convert M4A to WAV (if necessary)
    if filename.endswith(".m4a"):
        audio = AudioSegment.from_file(file_path, format="m4a")
        file_path = file_path.replace(".m4a", ".wav")
        audio.export(file_path, format="wav")

    # Transcribe audio to text
    transcribed_text = transcribe_audio(file_path)
    if not transcribed_text:
        return jsonify({"error": "Could not transcribe audio"}), 500

    # Summarize text
    summary = summarize_text(transcribed_text)

    # Count words
    word_count = len(transcribed_text.split())

    return jsonify({"summary": summary, "word_count": word_count})

if __name__ == "__main__":
    app.run(debug=True)

print(genai.__version__)
