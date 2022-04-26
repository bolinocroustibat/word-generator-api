import random
from typing import Tuple

import requests
from tortoise.contrib.mysql.functions import Rand

from config import ALLOWED_TYPES_EN, DICTIONNARY_EN_API_URL
from models import GeneratedWordEN, RealWordEN

from .alter_text import alter_text_en


async def generate_definition_en(percentage: float) -> str:
    type, definition, example = await get_random_definition_en()
    definition = await alter_text_en(text=definition, percentage=percentage)
    if type == "verb":
        generated_word = (
            await GeneratedWordEN.filter(type=type, tense="infinitive")
            .annotate(order=Rand())
            .order_by("order")
            .limit(1)
        )
        print(generated_word[0])
    elif type == "noun":
        generated_word = (
            await GeneratedWordEN.filter(type=type, number="s")
            .annotate(order=Rand())
            .order_by("order")
            .limit(1)
        )
    else:
        generated_word = (
            await GeneratedWordEN.filter(type=type)
            .annotate(order=Rand())
            .order_by("order")
            .limit(1)
        )
    return {
        "string": generated_word[0].string,
        "type": type,
        "definition": definition,
    }


async def get_random_definition_en() -> Tuple[str, str, str]:
    """
    Returns a random real word definition, type and example.
    """
    word = await RealWordEN.annotate(order=Rand()).order_by("order").limit(1)
    type, definition, example = await get_definition_en(word=word[0].string)
    while (not definition) or (type not in ALLOWED_TYPES_EN):
        print(
            f"Definition for word '{word[0]}' or type '{type}' not supported, trying another word and definition..."
        )
        word = await RealWordEN.annotate(order=Rand()).order_by("order").limit(1)
        type, definition, example = await get_definition_en(word=word[0].string)
    return type, definition, example


async def get_definition_en(word: str) -> Tuple[str, str, str]:
    """
    Returns the type, definition and example of a given word using the dictionaryapi.
    """
    response = requests.get(f"{DICTIONNARY_EN_API_URL}{word}")
    try:
        meanings: list = response.json()[0]["meanings"]
    except:
        print(f"Dictionaryapi error: {response.json()}")
        return None, None, None
    else:
        meaning: dict = random.choice(meanings)
        type: str = meaning["partOfSpeech"]
        definitions: list = meaning["definitions"]
        definition: str = random.choice(definitions)["definition"]
        example: str = random.choice(definitions).get("example", None)
        return type, definition, example
