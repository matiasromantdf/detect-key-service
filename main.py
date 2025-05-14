from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import essentia.standard as es
import os

app = FastAPI()

# Agregá esto para permitir CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Podés reemplazar "*" por el dominio de tu frontend
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
    
    return KeyResult(key=key, scale=scale, confidence=strength)
