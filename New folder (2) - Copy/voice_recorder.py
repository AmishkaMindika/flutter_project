from flask import Flask, jsonify, send_file
import sounddevice as sd
import numpy as np
import wave
import os
import sys
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.abspath(__file__))  # Save in the same folder as the script

# Audio settings optimized for speech recognition
SAMPLE_RATE = 16000  # 16kHz is better for speech recognition
DURATION = 120  # 120 seconds recording time
CHANNELS = 1  # Mono audio
DTYPE = np.int16  # Audio data type

# Function to record audio with improved quality
def record_audio():
    print("Preparing to record...")
    print(f"Sample rate: {SAMPLE_RATE} Hz, Duration: {DURATION} seconds, Channels: {CHANNELS}")
    
    # Give a short delay before starting
    print("Recording will start in 3 seconds...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    print("Recording started... Speak clearly into the microphone.")
    
    # Record audio for the specified duration
    try:
        audio_data = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, 
                           channels=CHANNELS, dtype=DTYPE)
        
        # Show a progress indicator
        for i in range(DURATION):
            if i % 10 == 0:  # Update every 10 seconds
                print(f"Recording: {i}/{DURATION} seconds completed")
            time.sleep(1)
        
        sd.wait()  # Wait for recording to complete
        print("Recording finished successfully.")
        
        # Normalize audio (scale to use full dynamic range)
        if np.max(np.abs(audio_data)) > 0:  # Avoid division by zero
            audio_data = audio_data * (32767 / np.max(np.abs(audio_data)))
            audio_data = audio_data.astype(np.int16)
            
        # Save as WAV file
        audio_file = os.path.join(app.config['UPLOAD_FOLDER'], 'recorded_audio.wav')
        
        with wave.open(audio_file, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)  # 2 bytes for int16
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(audio_data.tobytes())
            
        print(f"Audio saved to {audio_file}")
        
        # Check if file was created successfully
        if os.path.exists(audio_file):
            file_size = os.path.getsize(audio_file) / 1024  # Size in KB
            print(f"File size: {file_size:.2f} KB")
            if file_size < 1:
                print("Warning: File size is very small. Audio may not have been recorded properly.")
        else:
            print("Error: File was not created successfully.")
            
        return audio_file
        
    except Exception as e:
        print(f"Error during recording: {e}")
        return None

# Function to check microphone levels before recording
def check_mic_levels(duration=3):
    print("Checking microphone levels... Please speak normally.")
    try:
        # Record a short sample to check levels
        audio_sample = sd.rec(int(SAMPLE_RATE * duration), samplerate=SAMPLE_RATE, 
                             channels=CHANNELS, dtype=DTYPE)
        sd.wait()
        
        # Calculate volume level
        volume_norm = np.linalg.norm(audio_sample) / np.sqrt(len(audio_sample))
        print(f"Volume level: {volume_norm:.2f}")
        
        if volume_norm < 10:
            print("Warning: Audio level is very low. Please speak louder or move closer to the microphone.")
        elif volume_norm > 5000:
            print("Warning: Audio level is very high. Please speak softer or move away from the microphone.")
        else:
            print("Audio level is good.")
            
        return volume_norm
    except Exception as e:
        print(f"Error checking microphone: {e}")
        return 0

# API to start recording
@app.route('/start_recording', methods=['POST'])
def start_recording():
    check_mic_levels()  # Check mic levels first
    audio_file = record_audio()
    if audio_file:
        return jsonify({'message': 'Recording completed', 'file_path': audio_file})
    else:
        return jsonify({'message': 'Recording failed'}), 500

# API to get the recorded audio file
@app.route('/get_audio', methods=['GET'])
def get_audio():
    audio_file = os.path.join(app.config['UPLOAD_FOLDER'], 'recorded_audio.wav')
    if os.path.exists(audio_file):
        return send_file(audio_file, as_attachment=True)
    return jsonify({'message': 'No recorded file found'}), 404

# API to list available audio devices
@app.route('/list_devices', methods=['GET'])
def list_devices():
    devices = sd.query_devices()
    return jsonify({'devices': str(devices)})

if __name__ == '__main__':
    print("Audio Recording Program")
    print("----------------------")
    
    # List available audio devices
    print("\nAvailable audio devices:")
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        print(f"{i}: {device['name']} (inputs: {device['max_input_channels']}, outputs: {device['max_output_channels']})")
    
    # Check microphone levels
    check_mic_levels()
    
    # Record the audio
    record_audio()
    
    print("\nRecording complete. The audio file has been saved.")
    print("You can now run api_test.py to transcribe and analyze the recording.")
    
    # Stop the program after recording
    sys.exit(0)