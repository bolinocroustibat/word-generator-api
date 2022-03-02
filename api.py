import random
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import ALLOW_ORIGINS, DICTIONNARY_API_URL
from en.classify import classify_en
from en.get_definition import get_definition_en
from fr.classify import classify_fr
from helpers.generate import generate_word
from models import GenereratedWordEN, database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup() -> None:
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    if database.is_connected:
        await database.disconnect()


@app.get("/{lang}")
async def generate(lang: str):
    if lang not in ["fr", "en", "it", "es"]:
        raise HTTPException(status_code=400, detail="Invalid language")
    word: str = generate_word(lang=lang, not_existing=True)
    response: dict = {"string": word}
    if lang == "fr":
        word_classes: dict = classify_fr(word=word)
        response.update(word_classes)
    if lang == "en":
        word_classes: dict = classify_en(word=word)
        response.update(word_classes)
    return response


@app.get("/db/{lang}")
async def get_word_from_db(lang: str):
    if lang not in ["fr", "en"]:
        raise HTTPException(status_code=400, detail="Invalid language")
    if lang == "en":
        words = await GenereratedWordEN.objects.all()
    if lang == "fr":
        words = await GenereratedWordEN.objects.all()
    word = random.choice(list(words))
    return word


@app.get("/definition/{lang}/{word}")
async def get_definition(lang: str):
    
    
    # if lang == "en":
    #     return get_definition_en(word=word)
    # else:
    #     raise HTTPException(status_code=400, detail="Invalid language")
