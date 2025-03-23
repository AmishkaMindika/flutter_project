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
import pymongo
from bson.objectid import ObjectId
from datetime import datetime
import base64
import io

# Load environment variables
load_dotenv('api.env')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.abspath(__file__))

# MongoDB connection setup
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client['ice_breaker_app']
recordings_collection = db['recordings']

# Audio settings
SAMPLE_RATE = 44100  # 44.1kHz standard sampling rate
DURATION = 120  # 60 seconds of recording
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

# Function to save audio to MongoDB
def save_audio_to_db(audio_file, user_id="anonymous", prompt=""):
    # Read the audio file
    with open(audio_file, 'rb') as f:
        audio_data = f.read()
    
    # Convert to base64 for storage
    audio_base64 = base64.b64encode(audio_data).decode('utf-8')
    
    # Save to MongoDB
    record = {
        'user_id': user_id,
        'prompt': prompt,
        'audio_data': audio_base64,
        'timestamp': datetime.now()
    }
    
    # Insert and return the record ID
    result = recordings_collection.insert_one(record)
    return str(result.inserted_id)

# Function to get audio from MongoDB
def get_audio_from_db(record_id):
    record = recordings_collection.find_one({'_id': ObjectId(record_id)})
    if record and 'audio_data' in record:
        # Decode base64 audio data
        audio_data = base64.b64decode(record['audio_data'])
        return audio_data, record.get('prompt', '')
    return None, None

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

# Function to split audio data directly
def split_audio_data(audio_data, chunk_length=60):
    # Convert bytes to AudioSegment
    audio_file = io.BytesIO(audio_data)
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
def calculate_score(word_count, prompt_text, speech_text, max_word_count=300):
    # Base score based on word count (60% of total score)
    word_count_score = min((word_count / max_word_count) * 60, 60)
    
    # Similarity score (40% of total score)
    similarity_ratio = calculate_similarity(prompt_text, speech_text)
    similarity_score = similarity_ratio * 40
    
    # Total score
    total_score = word_count_score + similarity_score
    
    return round(total_score, 2), round(similarity_ratio * 100, 2)

# Function to save score to MongoDB
def save_score_to_db(record_id, transcribed_text, word_count, similarity_percentage, score):
    # Update the existing record with the results
    recordings_collection.update_one(
        {'_id': ObjectId(record_id)},
        {'$set': {
            'transcribed_text': transcribed_text,
            'word_count': word_count,
            'similarity_percentage': similarity_percentage,
            'score': score,
            'processed_at': datetime.now()
        }}
    )
    return record_id

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

# Process audio data directly
def process_audio_data(audio_data, prompt_text=""):
    # Split audio into smaller chunks
    chunk_files = split_audio_data(audio_data)

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
            #history-section {{
                margin-top: 40px;
                display: none;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            .user-section {{
                margin-bottom: 20px;
            }}
            input[type=text], input[type=email], input[type=password] {{
                width: 100%;
                padding: 12px 20px;
                margin: 8px 0;
                display: inline-block;
                border: 1px solid #ccc;
                border-radius: 4px;
                box-sizing: border-box;
            }}
        </style>
    </head>
    <body>
        <h1>Ice Breaker Speech Challenge</h1>
        
        <div class="user-section">
            <input type="text" id="user-name" placeholder="Your Name (optional)">
        </div>
        
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
            <div id="record-id" style="font-size: 12px; color: #888;"></div>
        </div>
        
        <button id="view-history" style="margin-top: 30px; background-color: #3498db;">View History</button>
        
        <div id="history-section">
            <h2>Your Recording History</h2>
            <table id="history-table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Prompt</th>
                        <th>Score</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="history-body">
                    <!-- History data will be loaded here -->
                </tbody>
            </table>
        </div>
        
        <script>
            // Store the current question
            let currentQuestion = document.getElementById('ice-breaker-text').textContent;
            let currentRecordId = null;
            
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
                
                const userName = document.getElementById('user-name').value || 'anonymous';
                
                fetch('/start_recording', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{
                        prompt: currentQuestion,
                        user_id: userName
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
                    document.getElementById('record-id').textContent = 'Record ID: ' + data.record_id;
                    currentRecordId = data.record_id;
                    this.disabled = false;
                }})
                .catch(error => {{
                    console.error('Error:', error);
                    document.getElementById('loading').style.display = 'none';
                    alert('An error occurred during recording. Please try again.');
                    this.disabled = false;
                }});
            }});
            
            document.getElementById('view-history').addEventListener('click', function() {{
                const historySection = document.getElementById('history-section');
                
                if (historySection.style.display === 'block') {{
                    historySection.style.display = 'none';
                    this.textContent = 'View History';
                }} else {{
                    const userName = document.getElementById('user-name').value || 'anonymous';
                    
                    fetch('/get_history', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json'
                        }},
                        body: JSON.stringify({{
                            user_id: userName
                        }})
                    }})
                    .then(response => response.json())
                    .then(data => {{
                        const historyBody = document.getElementById('history-body');
                        historyBody.innerHTML = '';
                        
                        if (data.recordings.length === 0) {{
                            historyBody.innerHTML = '<tr><td colspan="4">No recordings found</td></tr>';
                        }} else {{
                            data.recordings.forEach(recording => {{
                                const row = document.createElement('tr');
                                
                                // Date column
                                const dateCell = document.createElement('td');
                                const recordDate = new Date(recording.timestamp);
                                dateCell.textContent = recordDate.toLocaleString();
                                row.appendChild(dateCell);
                                
                                // Prompt column
                                const promptCell = document.createElement('td');
                                promptCell.textContent = recording.prompt;
                                row.appendChild(promptCell);
                                
                                // Score column
                                const scoreCell = document.createElement('td');
                                scoreCell.textContent = recording.score ? recording.score.toFixed(2) + '%' : 'N/A';
                                row.appendChild(scoreCell);
                                
                                // Actions column
                                const actionsCell = document.createElement('td');
                                
                                const playButton = document.createElement('button');
                                playButton.textContent = 'Play';
                                playButton.style.padding = '5px 10px';
                                playButton.style.marginRight = '5px';
                                playButton.addEventListener('click', function() {{
                                    window.location.href = '/play_audio/' + recording._id;
                                }});
                                actionsCell.appendChild(playButton);
                                
                                const viewButton = document.createElement('button');
                                viewButton.textContent = 'Details';
                                viewButton.style.padding = '5px 10px';
                                viewButton.addEventListener('click', function() {{
                                    window.location.href = '/recording_details/' + recording._id;
                                }});
                                actionsCell.appendChild(viewButton);
                                
                                row.appendChild(actionsCell);
                                historyBody.appendChild(row);
                            }});
                        }}
                        
                        historySection.style.display = 'block';
                        this.textContent = 'Hide History';
                    }})
                    .catch(error => {{
                        console.error('Error:', error);
                        alert('Failed to load history.');
                    }});
                }}
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
    # Get the prompt and user ID from the request
    data = request.get_json()
    prompt = data.get('prompt', '')
    user_id = data.get('user_id', 'anonymous')
    
    audio_file = record_audio()
    
    # Save audio to MongoDB
    record_id = save_audio_to_db(audio_file, user_id, prompt)
    
    # Process the recorded audio
    results = process_audio_file(audio_file, prompt)
    
    # Save the results to MongoDB
    save_score_to_db(
        record_id, 
        results['transcribed_text'], 
        results['full_word_count'], 
        results['similarity_percentage'], 
        results['score']
    )
    
    return jsonify({
        'message': 'Recording and processing completed',
        'transcribed_text': results['transcribed_text'],
        'word_count': results['full_word_count'],
        'score': results['score'],
        'similarity_percentage': results['similarity_percentage'],
        'record_id': record_id
    })

# API to get user recording history
@app.route('/get_history', methods=['POST'])
def get_history():
    data = request.get_json()
    user_id = data.get('user_id', 'anonymous')
    
    # Query MongoDB for user recordings
    recordings = list(recordings_collection.find(
        {'user_id': user_id},
        {'audio_data': 0}  # Exclude audio data for performance
    ).sort('timestamp', -1))  # Sort by newest first
    
    # Convert ObjectId to string for JSON serialization
    for recording in recordings:
        recording['_id'] = str(recording['_id'])
        
        # Convert datetime objects to ISO format strings
        if 'timestamp' in recording:
            recording['timestamp'] = recording['timestamp'].isoformat()
        if 'processed_at' in recording:
            recording['processed_at'] = recording['processed_at'].isoformat()
    
    return jsonify({
        'recordings': recordings
    })

# API to get the recorded audio file
@app.route('/get_audio', methods=['GET'])
def get_audio():
    audio_file = os.path.join(app.config['UPLOAD_FOLDER'], 'recorded_audio.wav')
    if os.path.exists(audio_file):
        return send_file(audio_file, as_attachment=True)
    return jsonify({'message': 'No recorded file found'}), 404

# API to play a specific recording
@app.route('/play_audio/<record_id>', methods=['GET'])
def play_audio(record_id):
    audio_data, prompt = get_audio_from_db(record_id)
    if audio_data:
        # Create a response with the audio data
        return Response(
            audio_data,
            mimetype='audio/wav',
            headers={
                'Content-Disposition': f'inline; filename=recording_{record_id}.wav'
            }
        )
    return jsonify({'message': 'Recording not found'}), 404

# Page to view recording details
@app.route('/recording_details/<record_id>', methods=['GET'])
def recording_details(record_id):
    # Get the recording from MongoDB
    recording = recordings_collection.find_one({'_id': ObjectId(record_id)})
    
    if not recording:
        return "Recording not found", 404
    
    # Format the data for display
    timestamp = recording.get('timestamp', datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
    prompt = recording.get('prompt', 'No prompt')
    transcribed_text = recording.get('transcribed_text', 'Not transcribed')
    word_count = recording.get('word_count', 'N/A')
    similarity = recording.get('similarity_percentage', 'N/A')
    score = recording.get('score', 'N/A')
    
    # Create the HTML page
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Recording Details</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1 {{
                color: #333;
            }}
            .details-container {{
                background-color: #f9f9f9;
                padding: 20px;
                border-radius: 5px;
                margin-top: 20px;
            }}
            .detail-row {{
                margin-bottom: 15px;
            }}
            .detail-label {{
                font-weight: bold;
                display: inline-block;
                width: 150px;
            }}
            .audio-container {{
                margin: 20px 0;
            }}
            button {{
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                margin-top: 20px;
            }}
            button:hover {{
                background-color: #45a049;
            }}
        </style>
    </head>
    <body>
        <h1>Recording Details</h1>
        
        <div class="details-container">
            <div class="detail-row">
                <span class="detail-label">Date:</span>
                <span>{timestamp}</span>
            </div>
            
            <div class="detail-row">
                <span class="detail-label">Prompt:</span>
                <span>{prompt}</span>
            </div>
            
            <div class="detail-row">
                <span class="detail-label">Word Count:</span>
                <span>{word_count}</span>
            </div>
            
            <div class="detail-row">
                <span class="detail-label">Relevance:</span>
                <span>{similarity}%</span>
            </div>
            
            <div class="detail-row">
                <span class="detail-label">Score:</span>
                <span>{score}%</span>
            </div>
        </div>
        
        <h2>Transcription</h2>
        <div class="details-container">
            <p>{transcribed_text}</p>
        </div>
        
        <div class="audio-container">
            <h2>Audio Recording</h2>
            <audio controls>
                <source src="/play_audio/{record_id}" type="audio/wav">
                Your browser does not support the audio element.
            </audio>
        </div>
        
        <button onclick="window.location.href='/'">Back to Home</button>
    </body>
    </html>
    """

# API to process existing audio file
@app.route('/process_audio', methods=['GET', 'POST'])
def process_existing_audio():
    data = request.get_json()
    record_id = data.get('record_id')
    
    if record_id:
        # Process from MongoDB
        audio_data, prompt = get_audio_from_db(record_id)
        if not audio_data:
            return jsonify({'message': 'Recording not found'}), 404
        
        results = process_audio_data(audio_data, prompt)
        
        # Save results to MongoDB
        save_score_to_db(
            record_id, 
            results['transcribed_text'], 
            results['full_word_count'], 
            results['similarity_percentage'], 
            results['score']
        )
    else:
        # Process local file
        audio_file = os.path.join(app.config['UPLOAD_FOLDER'], 'recorded_audio.wav')
        if not os.path.exists(audio_file):
            return jsonify({'message': 'No recorded file found'}), 404
        
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
