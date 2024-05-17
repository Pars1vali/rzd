import datetime
from enum import Enum
from typing import Union, List, Optional
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, Field


app = FastAPI(
    title="РЖД проверка служебных переговоров"
)



@app.get("/")
def init():
    return {"text": "Hello World!"}

@app.post("/audio")
async def upload_audio(file: UploadFile):
    content = await file.read()
    with open(f"uploaded_{file.filename}", "wb") as f:
        f.write(content)
    return {
        "correct":True
    }