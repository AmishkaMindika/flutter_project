import google.generativeai as genai
import Levenshtein
import json
import os

# Function to generate topic, compare to expected topic, and generate feedback
def compare_generated_topic_to_expected_with_feedback(api_key, text, expected_topic):
    genai.configure(api_key=api_key)
    
    # Use the correct model based on your available models
    model = genai.GenerativeModel("gemini-1.5-pro-latest")  # You can select the appropriate model
    
    # Generate a topic for the given text
    prompt = f"Generate a topic for the following text:\n{text}"
    response = model.generate_content(prompt)
    generated_topic = response.text.strip()  # Extract topic from the response
    
    # Compare the generated topic to the expected topic
    similarity_score = Levenshtein.ratio(expected_topic.lower(), generated_topic.lower())
    
    # Set a threshold for similarity, for example, 0.8 (80% similarity)
    threshold = 0.8
    result = "Passed" if similarity_score >= threshold else "Failed"
    
    # Generate feedback for improving speech abilities
    feedback = generate_speech_feedback(result, similarity_score)
    
    return generated_topic, similarity_score, result, feedback

# Function to generate feedback based on similarity score
def generate_speech_feedback(result, similarity_score):
    if result == "Failed":
        return f"Your topic generation is not fully aligned with the expected topic. It seems there may be some miscommunication or lack of clarity in conveying the central idea. Focus on improving the precision of your speech and try to be more concise in your explanations. Ensure that your key points are clearly articulated, and stay on topic throughout your discussion. Aim for a more structured approach to presenting your ideas."
    else:
        return f"Great job! Your topic generation closely matches the expected topic. You are on the right track. Keep practicing to ensure that you continue to express your thoughts clearly and with precision. Consider improving the flow of your ideas to make your speech even more effective."

# Function to load the transcribed text from file
def load_transcribed_text(filename="transcribed_text.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return data.get("transcribed_text", "")
    except FileNotFoundError:
        print(f"Error: {filename} not found. Using default text.")
        return ""
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filename}. Using default text.")
        return ""

# Example usage
if __name__ == "__main__":
    API_KEY = "AIzaSyDubSOYVgXUOHR_b-IsEJTNSs1SOI6vZns"  # Replace with your actual Gemini API key
    
    # Load transcribed text from file created by api_test.py
    transcribed_text = load_transcribed_text()
    
    # Use default text if no transcribed text is available
    if not transcribed_text:
        transcribed_text = """This is Santa. He has spent his whole life working on his farm every day from sunrise to sunset, following traditions passed down through generations, trusting in the land and seasons. But today, something is wrong. As he steps onto his field, his heart sinks. The last green paddy is dry, and there's no sign of rain. Despite his hard work and effort, his dreams are slipping away before his eyes."""
    
    # Define the expected topic manually
    expected_topic = "Farming Struggles due to Drought and Climate Change"
    
    # Get the generated topic, comparison result, similarity score, and feedback
    generated_topic, similarity_score, result, feedback = compare_generated_topic_to_expected_with_feedback(API_KEY, transcribed_text, expected_topic)
    
    print(f"Generated Topic: {generated_topic}")
    print(f"Similarity Score: {similarity_score}")
    print(f"Result: {result}")
    print(f"Feedback: {feedback}")