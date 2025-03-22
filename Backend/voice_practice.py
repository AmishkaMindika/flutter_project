from fastapi import FastAPI, File, UploadFile
import aiofiles
import google.generativeai as genai
import nltk
from nltk.tokenize import word_tokenize
import os

nltk.download('punkt')

# Initialize FastAPI
app = FastAPI()

# Configure Gemini AI (Replace with your API Key)
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Function to process speech-to-text using Gemini AI
async def speech_to_text(audio_path: str):
    # Here you integrate Gemini API for speech-to-text conversion
    response = genai.speech_to_text(audio_path)  # Mock function, replace with actual API call
    return response.get("text", "")

# Function to summarize text using Gemini AI
async def summarize_text(text: str):
    response = genai.summarize(text)  # Mock function, replace with actual API call
    return response.get("summary", "")

# Function to count words in text
def count_words(text: str):
    words = word_tokenize(text)
    return len(words)

# API Endpoint to handle voice practice mode
@app.post("/voice-practice/")
async def voice_practice(audio: UploadFile = File(...), topic: str = "General"):
    # Save uploaded audio file temporarily
    audio_path = f"temp_audio/{audio.filename}"
    os.makedirs("temp_audio", exist_ok=True)
    
    async with aiofiles.open(audio_path, "wb") as out_file:
        content = await audio.read()
        await out_file.write(content)

    # Convert speech to text
    transcribed_text = await speech_to_text(audio_path)

    # Summarize the text
    summarized_text = await summarize_text(transcribed_text)

    # Compare topic with summarized text (Simple keyword check)
    is_relevant = topic.lower() in summarized_text.lower()

    # Count words
    word_count = count_words(transcribed_text)

    # Define word count requirement (example: at least 50 words)
    required_word_count = 50
    meets_word_count = word_count >= required_word_count

    # Check if user passes
    if is_relevant and meets_word_count:
        result = {"status": "pass", "word_count": word_count, "summary": summarized_text}
    else:
        result = {"status": "fail", "word_count": word_count, "summary": summarized_text}

    # Clean up temp file
    os.remove(audio_path)

    return result
