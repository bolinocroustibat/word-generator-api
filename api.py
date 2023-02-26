from pathlib import Path
from typing import Optional

import nltk
import sentry_sdk
import toml
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.mysql.functions import Rand

from common import authenticate, generate_word_and_save
from config import ALLOW_ORIGINS, DATABASE_URL, ENVIRONMENT, SENTRY_DSN
from en import alter_text_en, generate_definition_en
from fr import alter_text_fr, generate_definition_fr
from models import GeneratedWordEN, GeneratedWordFR

# Load app name, version, commit variables from config file
# Need an absolute path for when we launch the scripts not from the project root dir (tweet command from cron, for example)
pyproject_filepath = Path(__file__).parent / "pyproject.toml"
config: dict = toml.load(pyproject_filepath)
APP_NAME: str = config["project"]["name"]
DESCRIPTION: str = config["project"]["description"]
VERSION: str = config["project"]["version"]

app = FastAPI(
    title=APP_NAME,
    description=DESCRIPTION,
    version=VERSION,
)

if ENVIRONMENT != "local":
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        release=f"{APP_NAME}@{VERSION}",
        environment=ENVIRONMENT,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # Sentry recommend adjusting this value in production,
        traces_sample_rate=1.0,
        # Experimental profiling
        _experiments={
            "profiles_sample_rate": 1.0,
        },
    )

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": ["models"]},
    generate_schemas=False,
    add_exception_handlers=True,
)

limiter = Limiter(key_func=get_remote_address)
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
    """
    Generate a random word and save it in DB.
    """
    if lang not in ["en", "fr", "it", "es"]:
        raise HTTPException(status_code=400, detail="Language not supported.")
    ip: str = request.client.host
    response: Optional[dict] = await generate_word_and_save(lang=lang, ip=ip)
    if response:
        return response
    else:
        raise HTTPException(status_code=500, detail="Too many retries.")


@app.get("/{lang}/get")
@limiter.limit("20/minute")
async def get_word_from_db(request: Request, lang: str):
    """
    Get a random generated word from DB.
    """
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
    Alter a text with random non existing words.
    """
    if lang == "en":
        return await alter_text_en(text, percentage)
    elif lang == "fr":
        return await alter_text_fr(text, percentage)
    else:
        raise HTTPException(status_code=400, detail="Language not supported.")


@app.get("/{lang}/definition")
@limiter.limit("3/minute")
async def get_definition(request: Request, lang: str):
    """
    Generate a random fake/altered dictionnary definition.
    """
    ip: str = request.client.host
    if lang == "en":
        return await generate_definition_en(percentage=0.5, ip=ip)
    elif lang == "fr":
        return await generate_definition_fr(percentage=0.6, ip=ip)
    else:
        raise HTTPException(status_code=400, detail="Language not supported.")


@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(authenticate)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/redoc", include_in_schema=False)
async def get_redoc_documentation(username: str = Depends(authenticate)):
    return get_redoc_html(openapi_url="/openapi.json", title="docs")


@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(authenticate)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)
