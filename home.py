import datetime
import io
from enum import Enum
from typing import Union, List, Optional
from fastapi import FastAPI, UploadFile, File
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pydub import AudioSegment
from backand import modal


app = FastAPI(
    title="РЖД проверка служебных переговоров"
)

@app.get("/")
def init():
    return {"text": "Hello World!"}

@app.post("/audio")
async def upload_audio(file: UploadFile):
    answer = None
    count_speech_voices = None
    file_name = file.filename.lower()

    if file_name.endswith('.mp3'):
        answer = 'mp3'
        file_content = await file.read()
        with open(f"{file_name}", "wb") as f:
            f.write(file_content)
        # audio_mp3 = AudioSegment.from_file(file_name, format="mp3")
        # audio_wav = audio_mp3.export("output_audio.wav", format="wav")
    elif file_name.endswith('.wav'):
        answer = 'wav'
        file_content = await file.read()
        with open(f"{file_name}", "wb") as f:
            f.write(file_content)
        count_speech_voices = modal.transribation(file_name)

    return {
        "file_name":file_name,
        "answer":answer,
        "count_speech_voices": count_speech_voices
    }