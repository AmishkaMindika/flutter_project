from flask import Flask, jsonify, send_file, render_template, Response, request
import sounddevice as sd
import numpy as np
import wave
import os
import sys
import requests
import speech_recognition as sr
from pydub import AudioSegment
import math
from dotenv import load_dotenv
import random
from difflib import SequenceMatcher

# Load environment variables
load_dotenv('api.env')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.abspath(__file__))

# Audio settings
SAMPLE_RATE = 44100  # 44.1kHz standard sampling rate
DURATION = 60  # 60 seconds of recording
CHANNELS = 1  # Mono audio

# Ice Breaker questions list
ICE_BREAKER_QUESTIONS = [
    "Tell us about a hobby you're passionate about.",
    "What's a skill you'd like to learn in the next year?",
    "Share a memorable travel experience you've had.",
    "If you could have dinner with any historical figure, who would it be and why?",
    "What's your favorite book or movie and why does it resonate with you?",
    "Tell us about a challenge you've overcome and what you learned from it.",
    "What's something most people don't know about you?",
    "If you could live anywhere in the world, where would it be?",
    "Share a personal goal you're currently working towards.",
    "What's the best advice someone has given you?",
    "Tell us about someone who has influenced your life significantly.",
    "What's a cause or issue you feel strongly about?",
    "Share a proud accomplishment from your life.",
    "If you had a time machine, which era would you visit?",
    "What's something you're looking forward to in the near future?",
    "Tell us about your ideal weekend.",
    "What's a lesson you've learned from a mistake?",
    "Share a tradition (family, cultural, personal) that's important to you.",
    "What's a quality you appreciate most in other people?",
    "If you could instantly master any skill, what would it be?"
]

# Function to get random ice breaker question
def get_random_ice_breaker():
    return random.choice(ICE_BREAKER_QUESTIONS)

# Function to record audio
def record_audio():
    print("Recording started...")

    # Record audio for the specified duration
    audio_data = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype=np.int16)
    sd.wait()  # Wait for recording to complete
    print("Recording finished.")

    # Save as WAV file
    audio_file = os.path.join(app.config['UPLOAD_FOLDER'], 'recorded_audio.wav')
    with wave.open(audio_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data.tobytes())

    print(f"Audio saved to {audio_file}")
    return audio_file

# Function to split long audio into smaller chunks (max 60 sec each)
def split_audio(audio_file, chunk_length=60):  # 60 seconds per chunk
    audio = AudioSegment.from_wav(audio_file)
    total_length = len(audio) / 1000  # Convert ms to seconds
    num_chunks = math.ceil(total_length / chunk_length)
    
    chunk_files = []
    for i in range(num_chunks):
        start_time = i * chunk_length * 1000  # Convert to ms
        end_time = min((i + 1) * chunk_length * 1000, len(audio))
        chunk = audio[start_time:end_time]
        
        chunk_filename = f"chunk_{i}.wav"
        chunk.export(chunk_filename, format="wav")
        chunk_files.append(chunk_filename)
    
    return chunk_files

# Function to convert audio to text
def audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio_data)  # Using Google STT API
    except sr.UnknownValueError:
        print(f"Could not understand audio in {audio_file}")
        return ""
    except sr.RequestError as e:
        print(f"Google STT API request failed: {e}")
        return ""

# Function to calculate similarity between two texts
def calculate_similarity(text1, text2):
    # Convert both texts to lowercase for better comparison
    text1 = text1.lower()
    text2 = text2.lower()
    
    # Use SequenceMatcher to get a similarity ratio
    return SequenceMatcher(None, text1, text2).ratio()

# Function to calculate score based on word count and prompt similarity
def calculate_score(word_count, prompt_text, speech_text, max_word_count=170):
    # Base score based on word count (60% of total score)
    word_count_score = min((word_count / max_word_count) * 100, 60)
    
    # Similarity score (40% of total score)
    similarity_ratio = calculate_similarity(prompt_text, speech_text)
    similarity_score = similarity_ratio * 100
    
    # Total score
    total_score = word_count_score + similarity_score
    
    return round(total_score, 2), round(similarity_ratio * 100, 2)

# Process the audio file
def process_audio_file(audio_file='recorded_audio.wav', prompt_text=""):
    # Split audio into smaller chunks
    chunk_files = split_audio(audio_file)

    full_text = ""

    # Process each chunk
    for chunk_file in chunk_files:
        text = audio_to_text(chunk_file)
        full_text += text + " "
        os.remove(chunk_file)  # Remove temporary chunk file

    # Count words in the full transcribed text
    full_word_count = len(full_text.split())

    # Calculate score based on word count and similarity to prompt
    score, similarity_percentage = calculate_score(full_word_count, prompt_text, full_text)

    return {
        'transcribed_text': full_text.strip(),
        'full_word_count': full_word_count,
        'score': score,
        'similarity_percentage': similarity_percentage
    }

# Create a HTML template for the home page
@app.route('/')
def home():
    ice_breaker = get_random_ice_breaker()
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ice Breaker Speech App</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                text-align: center;
            }}
            .question {{
                font-size: 24px;
                margin: 30px 0;
                padding: 20px;
                background-color: #f0f8ff;
                border-radius: 10px;
            }}
            button {{
                background-color: #4CAF50;
                color: white;
                padding: 15px 32px;
                text-align: center;
                font-size: 16px;
                margin: 10px 2px;
                cursor: pointer;
                border: none;
                border-radius: 5px;
            }}
            button:hover {{
                background-color: #45a049;
            }}
            .results {{
                margin-top: 20px;
                text-align: left;
                display: none;
            }}
            .loading {{
                display: none;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <h1>Ice Breaker Speech Challenge</h1>
        
        <div class="question">
            <p>Please speak about the following topic for up to 60 seconds:</p>
            <p><strong id="ice-breaker-text">{ice_breaker}</strong></p>
            <button id="new-question">Get New Question</button>
        </div>
        
        <button id="start-recording">Start Recording</button>
        <div class="loading" id="loading">Recording in progress... (60 seconds)</div>
        
        <div class="results" id="results">
            <h2>Results</h2>
            <h3>Transcription:</h3>
            <div id="transcription"></div>
            
            <h3>Stats:</h3>
            <div id="word-count"></div>
            <div id="similarity"></div>
            <div id="score"></div>
        </div>
        
        <script>
            // Store the current question
            let currentQuestion = document.getElementById('ice-breaker-text').textContent;
            
            document.getElementById('new-question').addEventListener('click', function() {{
                fetch('/get_ice_breaker')
                    .then(response => response.json())
                    .then(data => {{
                        document.getElementById('ice-breaker-text').textContent = data.question;
                        currentQuestion = data.question;
                    }});
            }});
            
            document.getElementById('start-recording').addEventListener('click', function() {{
                this.disabled = true;
                document.getElementById('loading').style.display = 'block';
                
                fetch('/start_recording', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{
                        prompt: currentQuestion
                    }})
                }})
                .then(response => response.json())
                .then(data => {{
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('results').style.display = 'block';
                    document.getElementById('transcription').textContent = data.transcribed_text;
                    document.getElementById('word-count').textContent = 'Word Count: ' + data.word_count;
                    document.getElementById('similarity').textContent = 'Relevance to Topic: ' + data.similarity_percentage.toFixed(2) + '%';
                    document.getElementById('score').textContent = 'Overall Score: ' + data.score.toFixed(2) + '%';
                    this.disabled = false;
                }})
                .catch(error => {{
                    console.error('Error:', error);
                    document.getElementById('loading').style.display = 'none';
                    alert('An error occurred during recording. Please try again.');
                    this.disabled = false;
                }});
            }});
        </script>
    </body>
    </html>
    """

# API to get a random ice breaker question
@app.route('/get_ice_breaker', methods=['GET'])
def get_ice_breaker():
    return jsonify({'question': get_random_ice_breaker()})

# API to start recording and process immediately
@app.route('/start_recording', methods=['POST'])
def start_recording():
    # Get the prompt from the request
    data = request.get_json()
    prompt = data.get('prompt', '')
    
    audio_file = record_audio()
    
    # Process the recorded audio
    results = process_audio_file(audio_file, prompt)
    
    return jsonify({
        'message': 'Recording and processing completed',
        'transcribed_text': results['transcribed_text'],
        'word_count': results['full_word_count'],
        'score': results['score'],
        'similarity_percentage': results['similarity_percentage']
    })

# API to get the recorded audio file
@app.route('/get_audio', methods=['GET'])
def get_audio():
    audio_file = os.path.join(app.config['UPLOAD_FOLDER'], 'recorded_audio.wav')
    if os.path.exists(audio_file):
        return send_file(audio_file, as_attachment=True)
    return jsonify({'message': 'No recorded file found'}), 404

# API to process existing audio file
@app.route('/process_audio', methods=['GET', 'POST'])
def process_existing_audio():
    audio_file = os.path.join(app.config['UPLOAD_FOLDER'], 'recorded_audio.wav')
    if not os.path.exists(audio_file):
        return jsonify({'message': 'No recorded file found'}), 404
    
    # Get the prompt from the request
    data = request.get_json()
    prompt = data.get('prompt', '')
    
    results = process_audio_file(audio_file, prompt)
    
    return jsonify({
        'transcribed_text': results['transcribed_text'],
        'word_count': results['full_word_count'],
        'score': results['score'],
        'similarity_percentage': results['similarity_percentage']
    })

if __name__ == '__main__':
    app.run(debug=True)
