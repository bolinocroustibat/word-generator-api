import random

import nltk
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from common.generate_word import generate_word_and_save
from config import ALLOW_ORIGINS
from en.generate_definition import generate_definition_en
from models import GenereratedWordEN, database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
app.state.database = database


nltk.download("averaged_perceptron_tagger")


@app.on_event("startup")
async def startup() -> None:
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    if database.is_connected:
        await database.disconnect()


@app.get("/{lang}/generate")
async def generate(lang: str, request: Request):
    if lang not in ["en", "fr", "it", "es"]:
        raise HTTPException(status_code=400, detail="Language not supported.")
    ip: str = request.client.host
    response: dict = await generate_word_and_save(lang=lang, ip=ip)
    return response


@app.get("/{lang}/get")
async def get_word_from_db(lang: str):
    if lang not in ["en", "fr"]:
        raise HTTPException(status_code=400, detail="Language not supported.")
    if lang == "en":
        words = await GenereratedWordEN.objects.all()
    if lang == "fr":
        words = await GenereratedWordEN.objects.all()
    word = random.choice(list(words))
    return word


@app.get("/{lang}/definition")
async def get_definition(lang: str):
    if lang == "en":
        return await generate_definition_en()
    else:
        raise HTTPException(status_code=400, detail="Language not supported.")
