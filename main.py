from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import essentia.standard as es
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class KeyResult(BaseModel):
    tono: str
    escala: str
    confianza: float

@app.get("/detect-key", response_model=KeyResult)
def detect_key(url: str = Query(...)):
    filename = "temp_audio.mp3"
    with open(filename, "wb") as f:
        f.write(requests.get(url).content)

    audio = es.MonoLoader(filename=filename)()
    tono, escala, confianza = es.KeyExtractor()(audio)
    os.remove(filename)
    
    return KeyResult(tono=tono, escala=escala, confianza=confianza)
