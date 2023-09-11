import random
from datetime import datetime

import requests
from tortoise.contrib.postgres.functions import Random

from config import ALLOWED_TYPES_EN, DICTIONNARY_EN_API_URL
from models import GeneratedDefinitionEN, GeneratedWordEN, RealWordEN

from .alter_text import alter_text_en


async def generate_definition_en(percentage: float, ip: str | None = None) -> dict:

    random_definition = await get_random_definition_en()
    real_string = random_definition["real_string"]
    type = random_definition["type"]
    definition = random_definition["definition"]

    if type == "verb":
        generated_word = (
            await GeneratedWordEN.filter(type=type, tense="infinitive")
            .annotate(order=Random())
            .order_by("order")
            .limit(1)
        )
    elif type == "noun":
        generated_word = (
            await GeneratedWordEN.filter(type=type, number="s")
            .annotate(order=Random())
            .order_by("order")
            .limit(1)
        )
    else:
        generated_word = (
            await GeneratedWordEN.filter(type=type)
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
    await GeneratedDefinitionEN.create(
        generated_word_id=generated_word[0].id,
        text=definition,
        date=datetime.utcnow(),
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

    while (not definition) or (type not in ALLOWED_TYPES_EN):
        if count > 0:
            print(
                f"Definition for word '{real_string}' or type '{type}' not supported, trying another word and definition..."  # noqa: E501
            )
        word = await RealWordEN.annotate(order=Random()).order_by("order").limit(1)
        real_string = word[0].string

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

    response = requests.get(f"{DICTIONNARY_EN_API_URL}{word}")

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
