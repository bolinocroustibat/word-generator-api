import random

import nltk
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from common.generate_word import generate_word_and_save
from config import ALLOW_ORIGINS
from en.generate_definition import generate_definition_en
from models import GenereratedWordEN, database

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
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
@limiter.limit("20/minute")
async def generate(request: Request, lang: str):
    if lang not in ["en", "fr", "it", "es"]:
        raise HTTPException(status_code=400, detail="Language not supported.")
    ip: str = request.client.host
    response: dict = await generate_word_and_save(lang=lang, ip=ip)
    if response:
        return response
    else:
        raise HTTPException(status_code=500, detail="Too many retries.")


@app.get("/{lang}/get")
@limiter.limit("20/minute")
async def get_word_from_db(request: Request, lang: str):
    if lang not in ["en", "fr"]:
        raise HTTPException(status_code=400, detail="Language not supported.")
    if lang == "en":
        words = await GenereratedWordEN.objects.all()
    if lang == "fr":
        words = await GenereratedWordEN.objects.all()
    word = random.choice(list(words))
    return word

@app.get("/{lang}/definition")
@limiter.limit("5/minute")
async def get_definition(request: Request, lang: str):
    if lang == "en":
        return await generate_definition_en()
    else:
        raise HTTPException(status_code=400, detail="Language not supported.")
