from typing import Optional

import nltk
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.mysql.functions import Rand

from common.generate_word import generate_word_and_save
from config import ALLOW_ORIGINS, APP_NAME, DATABASE_URL, DESCRIPTION, VERSION
from en import alter_text_en, generate_definition_en
from fr import alter_text_fr, generate_definition_fr
from models import GeneratedWordEN, GeneratedWordFR



limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title=APP_NAME, description=DESCRIPTION, version=VERSION)
register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": ["models"]},
    generate_schemas=False,
    add_exception_handlers=True,
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

nltk.download("averaged_perceptron_tagger")


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
    if lang == "en":
        word = await GeneratedWordEN.annotate(order=Rand()).order_by("order").limit(1)
        return {
            "string": word[0].string,
            "type": word[0].type,
            "number": word[0].number,
            "tense": word[0].tense,
        }
    elif lang == "fr":
        word = await GeneratedWordFR.annotate(order=Rand()).order_by("order").limit(1)
        return {
            "string": word[0].string,
            "type": word[0].type,
            "gender": word[0].gender,
            "number": word[0].number,
            "tense": word[0].tense,
            "conjug": word[0].conjug,
        }
    else:
        raise HTTPException(status_code=400, detail="Language not supported.")


@app.get("/{lang}/alter")
@limiter.limit("6/minute")
async def alter_text(
    request: Request, lang: str, text: str, percentage: Optional[float] = 0.4
):
    """
    Alter a POSTed text with random non existing words.
    """
    if lang == "en":
        return await alter_text_en(text=text, percentage=percentage)
    elif lang == "fr":
        return await alter_text_fr(text=text, percentage=percentage)
    else:
        raise HTTPException(status_code=400, detail="Language not supported.")


@app.get("/{lang}/definition")
@limiter.limit("3/minute")
async def get_definition(request: Request, lang: str):
    if lang == "en":
        return await generate_definition_en(percentage=0.3)
    elif lang == "fr":
        return await generate_definition_fr(percentage=0.4)
    else:
        raise HTTPException(status_code=400, detail="Language not supported.")
