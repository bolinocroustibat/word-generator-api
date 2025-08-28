import random
from datetime import UTC, datetime

import httpx
from dotenv import load_dotenv
from tortoise.contrib.postgres.functions import Random

from models import GeneratedDefinition, GeneratedWord, Language, RealWord

from .alter_text import alter_text_en

load_dotenv()

ALLOWED_TYPES_EN = ["noun", "verb", "adjective", "adverb"]
DICTIONNARY_EN_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"


async def generate_definition_en(percentage: float, ip: str | None = None) -> dict:
    random_definition = await get_random_definition_en()
    real_string = random_definition["real_string"]
    type = random_definition["type"]
    definition = random_definition["definition"]

    # Get English language ID
    english = await Language.get(code="en")

    if type == "verb":
        generated_word = (
            await GeneratedWord.filter(language=english, type=type, tense="infinitive")
            .annotate(order=Random())
            .order_by("order")
            .limit(1)
        )
    elif type == "noun":
        generated_word = (
            await GeneratedWord.filter(language=english, type=type, number="s")
            .annotate(order=Random())
            .order_by("order")
            .limit(1)
        )
    else:
        generated_word = (
            await GeneratedWord.filter(language=english, type=type)
            .annotate(order=Random())
            .order_by("order")
            .limit(1)
        )
    generated_string: str = generated_word[0].string
    definition = await alter_text_en(
        text=definition,
        percentage=percentage,
        forced_replacements={real_string: generated_string},
    )

    # Save definition in DB
    if not ip:
        ip = "localhost"
    await GeneratedDefinition.create(
        generated_word_id=generated_word[0].id,
        text=definition,
        date=datetime.now(UTC),
        ip=ip,
    )

    return {
        "string": generated_string,
        "type": type,
        "definition": definition,
    }


async def get_random_definition_en() -> dict:
    """
    Returns a random real word definition, type and example.
    """
    count = 0
    definition = None
    real_string: str | None = None
    type: str | None = None
    example: str | None = None

    # Get English language ID
    english = await Language.get(code="en")

    while (not definition) or (type not in ALLOWED_TYPES_EN):
        if count > 0:
            print(
                f"Definition for word '{real_string}' or type '{type}' not supported, trying another word and definition..."
            )
        word = (
            await RealWord.filter(language=english)
            .annotate(order=Random())
            .order_by("order")
            .limit(1)
        )
        real_string = word[0].string

        if real_string:
            definition_dict: dict = await get_definition_from_word_en(word=real_string)
            type = definition_dict["type"]
            definition = definition_dict["definition"]
            example = definition_dict["example"]

        count += 1

    return {
        "real_string": real_string,
        "type": type,
        "definition": definition,
        "example": example,
    }


async def get_definition_from_word_en(word: str) -> dict:
    """
    Returns the type, definition and example of a given word using the dictionaryapi.
    """
    type: str | None = None
    definition: str | None = None
    example: str | None = None

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DICTIONNARY_EN_API_URL}{word}")

        try:
            meanings: list = response.json()[0]["meanings"]
        except Exception:
            print(f"DictionaryAPI error: {response.json()}")
        else:
            meaning: dict = random.choice(meanings)
            type = meaning["partOfSpeech"]
            definitions: list = meaning["definitions"]
            definition = random.choice(definitions)["definition"]
            example = random.choice(definitions).get("example", None)

    return {"type": type, "definition": definition, "example": example}
