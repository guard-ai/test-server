import requests
import json
import uvicorn
import numpy as np
import sounddevice as sd
import time
from fastapi import FastAPI, Request

app = FastAPI()
# Buffer to accumulate audio samples
audio_buffer = np.array([])
# Constants for Whisper AI
SAMPLE_RATE = 16000
N_FFT = 400
HOP_LENGTH = 160
CHUNK_LENGTH = 30
N_SAMPLES = CHUNK_LENGTH * SAMPLE_RATE

def process_audio(indata, frames, time, status):
    global audio_buffer
    audio_buffer = np.append(audio_buffer, indata.flatten())

    while len(audio_buffer) >= N_SAMPLES:
        chunk = audio_buffer[:N_SAMPLES]
        audio_buffer = audio_buffer[N_SAMPLES:]

        print("Processing chunk with shape:", chunk.shape)
        response = requests.post("http://localhost:8888/audio_to_text", json=chunk.tolist())

@app.post("/process_and_post")
async def process_and_post(request: Request):
    with sd.InputStream(callback=process_audio, channels=1, samplerate=SAMPLE_RATE):
        print("Streaming audio. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)  
        except KeyboardInterrupt:
            print("\nStopped.")
            return

    

def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()