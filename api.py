import random

import nltk
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from common.generate import generate_word
from config import ALLOW_ORIGINS
from en.classify import classify_en
from en.get_definition import alter_definition, get_random_definition
from fr.classify import classify_fr
from models import GenereratedWordEN, RealWordEN, database

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
async def generate(lang: str):
    if lang not in ["en", "fr", "it", "es"]:
        raise HTTPException(status_code=400, detail="Language not supported.")
    word: str = generate_word(lang=lang, not_existing=True)
    response: dict = {"string": word}
    if lang == "fr":
        word_classes: dict = classify_fr(word=word)
        response.update(word_classes)
    if lang == "en":
        word_classes: dict = classify_en(word=word)
        response.update(word_classes)
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
        type, definition, example = await get_random_definition()
        definition = await alter_definition(definition=definition, percentage=0.2)
        if type == "verb":
            generated_words = await GenereratedWordEN.objects.all(
                type=type, tense="infinitive"
            )
        else:
            generated_words = await GenereratedWordEN.objects.all(type=type)
        string = random.choice(list(generated_words)).string
        return {
            "string": string,
            "type": type,
            "definition": definition,
        }
    else:
        raise HTTPException(status_code=400, detail="Language not supported.")

    # if lang == "en":
    #     return get_definition_en(word=word)
    # else:
    #     raise HTTPException(status_code=400, detail="Invalid language")
