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
    if file_name.endswith('.mp3'):
        answer =  'mp3'
    elif file_name.endswith('.wav'):
        answer = 'wav'
        file_content = await file.read()
        with open(f"{file_name}", "wb") as f:
            f.write(file_content)
        modal.transribation(file_name)

    return {
        "file_name":file_name,
        "answer":answer
    }