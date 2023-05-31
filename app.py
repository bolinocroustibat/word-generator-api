from pathlib import Path
from typing import Optional

import nltk
import sentry_sdk
import toml
from litestar import Litestar, get, Request
from litestar.config.cors import CORSConfig
from litestar.middleware.rate_limit import RateLimitConfig
from litestar.exceptions import HTTPException
from litestar.openapi import OpenAPIConfig
from litestar.plugins.tortoise_orm import TortoiseORMPlugin
from tortoise import Tortoise
from tortoise.connection import connections
from tortoise.contrib.mysql.functions import Rand

from common import generate_word_and_save
from config import ALLOW_ORIGINS, DATABASE_URL, ENVIRONMENT, SENTRY_DSN
from en import alter_text_en, generate_definition_en
from fr import alter_text_fr, generate_definition_fr
from models import (
    GeneratedDefinitionEN,
    GeneratedDefinitionFR,
    GeneratedWordEN,
    GeneratedWordFR,
)

# Load app name, version, commit variables from config file
# Need an absolute path for when we launch the scripts not from the project root dir (tweet command from cron, for example)  # noqa: E501
pyproject_filepath = Path(__file__).parent / "pyproject.toml"
config: dict = toml.load(pyproject_filepath)
APP_NAME: str = config["project"]["name"]
DESCRIPTION: str = config["project"]["description"]
VERSION: str = config["project"]["version"]

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

nltk.download("averaged_perceptron_tagger")


@get("/{lang}/word/generate", tags=["word"])
async def generate_word(request: Request, lang: str):
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


@get("/{lang}/word/get", tags=["word"])
async def get_random_word_from_db(request: Request, lang: str):
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


@get("/{lang}/definition/generate", tags=["definition"])
async def generate_definition(request: Request, lang: str):
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


@get("/{lang}/definition/get", tags=["definition"])
async def get_random_definition_from_db(request: Request, lang: str):
    """
    Get a random generated definition from DB.
    """
    if lang == "en":
        definition = (
            await GeneratedDefinitionEN.annotate(order=Rand())
            .order_by("order")
            .limit(1)
            .prefetch_related("generated_word")
        )
        return {
            "string": definition[0].generated_word.string,
            "definition": definition[0].text,
        }
    elif lang == "fr":
        definition = (
            await GeneratedDefinitionFR.annotate(order=Rand())
            .order_by("order")
            .limit(1)
            .prefetch_related("generated_word")
        )
        return {
            "string": definition[0].generated_word.string,
            "definition": definition[0].text,
        }
    else:
        raise HTTPException(status_code=400, detail="Language not supported.")


@get("/{lang}/alter", tags=["alter"])
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


cors_config = CORSConfig(allow_origins=ALLOW_ORIGINS)

rate_limit_config = RateLimitConfig(
    rate_limit=("minute", 5), exclude=["/schema", "/docs", "/redoc", "/openapi.json"]
)


async def init_tortoise() -> None:
    await Tortoise.init(db_url=DATABASE_URL, modules={"models": ["models"]})
    await Tortoise.generate_schemas()


async def shutdown_tortoise() -> None:
    await connections.close_all()


app = Litestar(
    route_handlers=[
        generate_word,
        get_random_word_from_db,
        generate_definition,
        get_random_definition_from_db,
        alter_text,
    ],
    openapi_config=OpenAPIConfig(
        title=APP_NAME, version=VERSION, description=DESCRIPTION
    ),
    cors_config=cors_config,
    middleware=[rate_limit_config.middleware],
    on_startup=[init_tortoise],
    on_shutdown=[shutdown_tortoise],
    plugins=[TortoiseORMPlugin()],
)
