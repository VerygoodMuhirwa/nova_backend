import numpy as np
import soundfile as sf
import cv2
import asyncio
import base64
import pygame  #
import os
def init_pygame_audio():
    try:
        # Optionally, check if running in a Docker environment
        if os.environ.get('RUNNING_IN_DOCKER', 'false').lower() == 'true':
            print("Running in Docker, skipping pygame.mixer.init()")
            return
        # Initialize Pygame audio if not running in Docker
        pygame.mixer.init()
    except pygame.error as e:
        print(f"Error initializing audio: {e}")

init_pygame_audio()


# Function to generate and save an alert sound
def generate_alert_sound():
    frequency = 1000  # Frequency in Hertz (1kHz tone)
    duration = 0.001  # Duration in seconds
    silence_duration = 0.001  # Duration of silence between beeps

    # Generate tone
    tone = generate_tone(frequency, duration)
    silence = np.zeros(int(44100 * silence_duration))
    beep_sequence = np.concatenate([tone, silence, tone, silence, tone])

    # Save the sequence as a .wav file
    sf.write('alert.wav', beep_sequence, 44100)

def generate_tone(frequency, duration, sample_rate=44100, amplitude=0.5):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave

def play_alert_sound():
    # Load the alert sound
    pygame.mixer.music.load('alert.wav')
    pygame.mixer.music.play()  # Play the sound

generate_alert_sound()

async def capture_video():
    cap = cv2.VideoCapture(0)  # Open the default camera

    while True:
        ret, frcame = cap.read()
        if not ret:
            break
        # Process the frame as needed (for example, face detection)
        # Encode frame to send via WebSocket
        _, buffer = cv2.imencode('.jpg', frame)
        frame_encoded = base64.b64encode(buffer).decode('utf-8')


        await asyncio.sleep(0.03)  # Control the frame rate (30 FPS)

    cap.release()
