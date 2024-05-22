import datetime
import io, os
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
    speech_valid, text, type_problem = None, None, None
    file_name = file.filename.lower()

    if file_name.endswith('.mp3'):
        file_content = await file.read()
        with open(file_name, "wb") as f:
            f.write(file_content)
        audio = AudioSegment.from_mp3(file_name)
        audio.export("output.wav", format="wav")
        speech_valid, type_problem, text = modal.transribation("output.wav")
    elif file_name.endswith('.wav'):
        file_content = await file.read()
        with open(file_name, "wb") as f:
            f.write(file_content)
        speech_valid, type_problem, text = modal.transribation(file_name)

    return {
        "speech_valid":speech_valid,
        "text": text,
        "type_problem":type_problem
    }