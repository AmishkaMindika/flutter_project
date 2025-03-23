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
import threading
import time

# Load environment variables
load_dotenv('api.env')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.abspath(__file__))

# Audio settings
SAMPLE_RATE = 44100  # 44.1kHz standard sampling rate
DURATION = 60  # 60 seconds of recording
CHANNELS = 1  # Mono audio

# Global variable for recording control
recording_active = False
recording_thread = None
audio_data = None

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

# Function to record audio with stop capability
def record_audio_thread():
    global recording_active, audio_data
    print("Recording started...")
    
    # Set up the stream
    audio_data = np.array([], dtype=np.int16)
    stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype=np.int16)
    stream.start()
    
    # Record until stopped or max duration reached
    start_time = time.time()
    recording_active = True
    
    while recording_active and (time.time() - start_time) < DURATION:
        buffer, overflowed = stream.read(SAMPLE_RATE)  # Read 1 second of audio
        audio_data = np.append(audio_data, buffer.flatten())
    
    # Stop and close the stream
    stream.stop()
    stream.close()
    recording_active = False
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

# Function to stop recording
def stop_recording():
    global recording_active
    recording_active = False
    if recording_thread is not None:
        recording_thread.join()  # Wait for the recording thread to complete
    return os.path.join(app.config['UPLOAD_FOLDER'], 'recorded_audio.wav')

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
    word_count_score = min((word_count / max_word_count) * 60, 60)
    
    # Similarity score (40% of total score)
    similarity_ratio = calculate_similarity(prompt_text, speech_text)
    similarity_score = similarity_ratio * 40
    
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
            button:disabled {{
                background-color: #cccccc;
                cursor: not-allowed;
            }}
            .stop-btn {{
                background-color: #f44336;
                display: none;
            }}
            .stop-btn:hover {{
                background-color: #d32f2f;
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
            .timer-container {{
                margin: 20px auto;
                width: 300px;
                display: none;
            }}
            .timer {{
                font-size: 36px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .timer-bar {{
                height: 20px;
                background-color: #f0f8ff;
                border-radius: 10px;
                overflow: hidden;
            }}
            .timer-progress {{
                height: 100%;
                width: 100%;
                background-color: #4CAF50;
                transition: width 1s linear;
            }}
            .timer-red {{
                background-color: #FF6347;
            }}
            .new-question-btn {{
                background-color: #2196F3;
            }}
            .new-question-btn:hover {{
                background-color: #0b7dda;
            }}
            .button-container {{
                display: flex;
                justify-content: center;
                gap: 10px;
            }}
        </style>
    </head>
    <body>
        <h1>Ice Breaker Speech Challenge</h1>
        
        <div class="question">
            <p>Please speak about the following topic for up to 60 seconds:</p>
            <p><strong id="ice-breaker-text">{ice_breaker}</strong></p>
        </div>
        
        <div class="button-container">
            <button id="new-question" class="new-question-btn">Get New Question</button>
            <button id="start-recording">Start Recording</button>
            <button id="stop-recording" class="stop-btn">Stop Recording</button>
        </div>
        
        <div class="timer-container" id="timer-container">
            <div class="timer" id="timer">60</div>
            <div class="timer-bar">
                <div class="timer-progress" id="timer-progress"></div>
            </div>
        </div>
        
        <div class="loading" id="loading">Processing recording...</div>
        
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
            let timerInterval;
            let recordingInProgress = false;
            
            // Get DOM elements
            const startButton = document.getElementById('start-recording');
            const stopButton = document.getElementById('stop-recording');
            const newQuestionButton = document.getElementById('new-question');
            const timerContainer = document.getElementById('timer-container');
            const loadingElement = document.getElementById('loading');
            const resultsElement = document.getElementById('results');
            
            // New Question button
            newQuestionButton.addEventListener('click', function() {{
                fetch('/get_ice_breaker')
                    .then(response => response.json())
                    .then(data => {{
                        document.getElementById('ice-breaker-text').textContent = data.question;
                        currentQuestion = data.question;
                    }});
            }});
            
            function updateTimer(timeLeft, duration) {{
                document.getElementById('timer').textContent = timeLeft;
                const progressBar = document.getElementById('timer-progress');
                const percentage = (timeLeft / duration) * 100;
                progressBar.style.width = percentage + '%';
                
                // Change color when less than 10 seconds remain
                if (timeLeft <= 10) {{
                    progressBar.classList.add('timer-red');
                }} else {{
                    progressBar.classList.remove('timer-red');
                }}
            }}
            
            function startTimer(duration) {{
                let timeLeft = duration;
                timerContainer.style.display = 'block';
                updateTimer(timeLeft, duration);
                
                timerInterval = setInterval(function() {{
                    timeLeft--;
                    updateTimer(timeLeft, duration);
                    
                    if (timeLeft <= 0) {{
                        clearInterval(timerInterval);
                        stopRecording();
                    }}
                }}, 1000);
            }}
            
            function stopTimerAndReset() {{
                clearInterval(timerInterval);
                timerContainer.style.display = 'none';
            }}
            
            function stopRecording() {{
                if (!recordingInProgress) return;
                
                recordingInProgress = false;
                
                // Show processing message
                loadingElement.style.display = 'block';
                
                // Hide stop button, show start button
                stopButton.style.display = 'none';
                
                // Stop the timer
                stopTimerAndReset();
                
                // Call the API to stop recording
                fetch('/stop_recording', {{
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
                    loadingElement.style.display = 'none';
                    resultsElement.style.display = 'block';
                    document.getElementById('transcription').textContent = data.transcribed_text;
                    document.getElementById('word-count').textContent = 'Word Count: ' + data.word_count;
                    document.getElementById('similarity').textContent = 'Relevance to Topic: ' + data.similarity_percentage.toFixed(2) + '%';
                    document.getElementById('score').textContent = 'Overall Score: ' + data.score.toFixed(2) + '%';
                    
                    // Re-enable buttons
                    startButton.disabled = false;
                    newQuestionButton.disabled = false;
                }})
                .catch(error => {{
                    console.error('Error:', error);
                    loadingElement.style.display = 'none';
                    alert('An error occurred during recording. Please try again.');
                    
                    // Re-enable buttons
                    startButton.disabled = false;
                    newQuestionButton.disabled = false;
                }});
            }}
            
            // Start Recording button
            startButton.addEventListener('click', function() {{
                // Disable start and new question buttons
                this.disabled = true;
                newQuestionButton.disabled = true;
                
                // Show stop button
                stopButton.style.display = 'inline-block';
                
                // Hide results and show timer
                resultsElement.style.display = 'none';
                
                // Set recording in progress flag
                recordingInProgress = true;
                
                // Start the timer countdown
                startTimer(DURATION);
                
                // Start recording
                fetch('/start_recording', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }}
                }});
            }});
            
            // Stop Recording button
            stopButton.addEventListener('click', stopRecording);
            
            // Set the global duration for JavaScript
            const DURATION = {DURATION};
        </script>
    </body>
    </html>
    """

# API to get a random ice breaker question
@app.route('/get_ice_breaker', methods=['GET'])
def get_ice_breaker():
    return jsonify({'question': get_random_ice_breaker()})

# API to start recording
@app.route('/start_recording', methods=['POST'])
def start_recording():
    global recording_thread
    
    # Start the recording in a separate thread
    recording_thread = threading.Thread(target=record_audio_thread)
    recording_thread.start()
    
    return jsonify({'message': 'Recording started'})

# API to stop recording and process
@app.route('/stop_recording', methods=['POST'])
def stop_recording_api():
    # Get the prompt from the request
    data = request.get_json()
    prompt = data.get('prompt', '')
    
    # Stop the recording
    audio_file = stop_recording()
    
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
