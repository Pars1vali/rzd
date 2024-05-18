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
    speech_valid, text, type_problem = None, None, None
    file_name = file.filename.lower()

    if file_name.endswith('.mp3'):
        pass
    elif file_name.endswith('.wav'):
        file_content = await file.read()
        with open(f"{file_name}", "wb") as f:
            f.write(file_content)
        speech_valid, type_problem, text = modal.transribation(file_name)

    return {
        "speech_valid":speech_valid,
        "text": text,
        "type_problem":type_problem
    }