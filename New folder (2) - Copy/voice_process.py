import os
import requests
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import math
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = 'https://api.gemini.com/v1/summarize'  # Update if needed

# Function to split long audio into smaller chunks (max 60 sec each)
def split_audio(audio_file, chunk_length=60):  # 60 seconds per chunk
    try:
        print(f"Loading audio file: {audio_file}")
        audio = AudioSegment.from_wav(audio_file)
        total_length = len(audio) / 1000  # Convert ms to seconds
        print(f"Audio file length: {total_length} seconds")
        
        num_chunks = math.ceil(total_length / chunk_length)
        print(f"Splitting into {num_chunks} chunks...")
        
        chunk_files = []
        for i in range(num_chunks):
            start_time = i * chunk_length * 1000  # Convert to ms
            end_time = min((i + 1) * chunk_length * 1000, len(audio))
            chunk = audio[start_time:end_time]
            
            chunk_filename = f"chunk_{i}.wav"
            chunk.export(chunk_filename, format="wav")
            chunk_files.append(chunk_filename)
            print(f"Created chunk: {chunk_filename}")
        
        return chunk_files
    except Exception as e:
        print(f"Error splitting audio: {str(e)}")
        return []

# Function to convert audio to text with improved error handling
def audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    try:
        print(f"Processing audio file: {audio_file}")
        with sr.AudioFile(audio_file) as source:
            print(f"Recording audio from {audio_file}")
            audio_data = recognizer.record(source)
        
        print("Sending to Google Speech Recognition API...")
        text = recognizer.recognize_google(audio_data)
        print(f"Successfully transcribed {len(text)} characters")
        return text
    except sr.UnknownValueError:
        print(f"Google Speech Recognition could not understand audio in {audio_file}")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""
    except Exception as e:
        print(f"Unexpected error transcribing audio: {str(e)}")
        return ""

# Alternative function for handling problematic audio files
def transcribe_with_silence_splitting(audio_file):
    try:
        print("Trying alternative transcription method with silence splitting...")
        # Load audio file
        sound = AudioSegment.from_wav(audio_file)
        
        # Split audio where silence is 700ms or more and get chunks
        chunks = split_on_silence(
            sound,
            min_silence_len=700,
            silence_thresh=sound.dBFS-14,
            keep_silence=500
        )
        
        print(f"Audio split into {len(chunks)} chunks based on silence")
        
        # Create a directory to store the audio chunks
        if not os.path.isdir("audio_chunks"):
            os.mkdir("audio_chunks")
            
        # Process each chunk
        whole_text = ""
        recognizer = sr.Recognizer()
        
        for i, audio_chunk in enumerate(chunks):
            # Export chunk and save it in the audio_chunks directory
            chunk_filename = os.path.join("audio_chunks", f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            
            # Recognize the chunk
            with sr.AudioFile(chunk_filename) as source:
                audio_listened = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_listened)
                    whole_text += text + " "
                    print(f"Chunk {i}: {text}")
                except sr.UnknownValueError:
                    print(f"Could not understand chunk {i}")
                except Exception as e:
                    print(f"Error processing chunk {i}: {str(e)}")
        
        # Clean up chunk files
        import shutil
        if os.path.exists("audio_chunks"):
            shutil.rmtree("audio_chunks")
            
        return whole_text
    except Exception as e:
        print(f"Error in alternative transcription method: {str(e)}")
        return ""

# Function to get summary from Gemini API
def get_summary(text):
    if not text.strip():
        print("No text to summarize")
        return "No text to summarize"
        
    try:
        print("Requesting summary from Gemini API...")
        headers = {'Authorization': f'Bearer {GEMINI_API_KEY}'}
        response = requests.post(GEMINI_API_URL, json={'text': text}, headers=headers)
        
        if response.status_code != 200:
            print(f"API request failed with status code {response.status_code}: {response.text}")
            return "API request failed"
            
        summary = response.json().get('summary', 'No summary available')
        print("Summary received")
        return summary
    except Exception as e:
        print(f"Error getting summary: {str(e)}")
        return "Error getting summary"

# Function to calculate score based on word count
def calculate_score(word_count, max_word_count=300):
    score = (word_count / max_word_count) * 100  # Calculate percentage score
    return min(score, 100)  # Ensure max score is 100%

# Function to save transcribed text to a file
def save_transcribed_text(text, filename="transcribed_text.json"):
    try:
        data = {"transcribed_text": text}
        with open(filename, "w") as file:
            json.dump(data, file)
        print(f"Transcribed text saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving transcribed text: {str(e)}")
        return False

# Process the audio file with multiple methods if needed
def process_audio_file():
    audio_file = 'recorded_audio.wav'  # Directly use the WAV file
    
    # Check if file exists
    if not os.path.exists(audio_file):
        print(f"Error: Audio file '{audio_file}' not found!")
        return {
            'transcribed_text': "",
            'summary': "No audio file found",
            'full_word_count': 0,
            'score': 0
        }
    
    print(f"Found audio file: {audio_file}")
    
    # Try standard chunk-based method first
    chunk_files = split_audio(audio_file)
    full_text = ""
    
    # Process each chunk
    if chunk_files:
        for chunk_file in chunk_files:
            text = audio_to_text(chunk_file)
            full_text += text + " "
            try:
                os.remove(chunk_file)  # Remove temporary chunk file
            except:
                pass
    
    # If standard method didn't work well, try alternative method
    if not full_text.strip():
        print("Standard transcription failed. Trying alternative method...")
        full_text = transcribe_with_silence_splitting(audio_file)
    
    # If still no text, provide error message
    if not full_text.strip():
        print("All transcription methods failed. Please check the audio file.")
        return {
            'transcribed_text': "",
            'summary': "Transcription failed",
            'full_word_count': 0,
            'score': 0
        }
    
    # Save the transcribed text to a file for summary.py to use
    save_transcribed_text(full_text.strip())
    
    # Get summary of the full transcribed text
    summary = get_summary(full_text)
    
    # Count words in the full transcribed text
    full_word_count = len(full_text.split())
    
    # Calculate score based on word count
    score = calculate_score(full_word_count)
    
    return {
        'transcribed_text': full_text.strip(),
        'summary': summary,
        'full_word_count': full_word_count,
        'score': score
    }

if __name__ == "__main__":
    print("Starting audio processing...")
    
    # Execute the process
    result = process_audio_file()
    
    # Print the results
    print("\n--- Voice Processing Results ---")
    if result['transcribed_text']:
        print("Transcription successful!")
        print("Transcribed Text:", result['transcribed_text'])
        print("Summary:", result['summary'])
        print("Full Word Count:", result['full_word_count'])
        print("Score:", result['score'], "%")
        
        # Import and run the summary analysis with the transcribed text
        try:
            print("\nRunning topic analysis on transcribed text...")
            import subprocess
            subprocess.run(["python", "summary.py"])
        except Exception as e:
            print(f"Error running summary.py: {str(e)}")
    else:
        print("Transcription failed. No text was produced from the audio file.")
        print("Please check that your audio file is valid and properly formatted.")
        print("Make sure you have all required dependencies installed:")
        print("  - SpeechRecognition")
        print("  - pydub")
        print("  - pyaudio")
        print("For WAV file support, you may also need ffmpeg installed on your system.")