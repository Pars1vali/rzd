import datetime
import io
from enum import Enum
from typing import Union, List, Optional
from fastapi import FastAPI, UploadFile, File
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
    file_name = file.filename.lower()
    len_nonsilent_ranges = 0

    if file_name.endswith('.mp3'):
        answer = 'mp3'
        file_content = await file.read()
        with open(f"{file_name}", "wb") as f:
            f.write(file_content)

        audio_mp3 = AudioSegment.from_mp3(file_name)
        audio_wav = audio_mp3.export("output_audio.wav", format="wav")
    elif file_name.endswith('.wav'):
        answer = 'wav'
        file_content = await file.read()
        with open(f"{file_name}", "wb") as f:
            f.write(file_content)
        len_nonsilent_ranges = modal.transribation(file_name)

    return {
        "file_name":file_name,
        "answer":answer,
        "len_nonsilent_ranges": len_nonsilent_ranges
    }