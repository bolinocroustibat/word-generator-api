import random
from typing import Tuple

import requests

from config import ALLOWED_TYPES_EN, DICTIONNARY_EN_API_URL
from models import GenereratedWordEN, RealWordEN
from .alter_text import alter_text_en


async def generate_definition_en(percentage: float) -> str:
    type, definition, example = await get_random_definition_en()
    definition = await alter_text_en(text=definition, percentage=percentage)
    if type == "verb":
        generated_words = await GenereratedWordEN.objects.all(
            type=type, tense="infinitive"
        )
    elif type == "noun":
        generated_words = await GenereratedWordEN.objects.all(type=type, number="s")
    else:
        generated_words = await GenereratedWordEN.objects.all(type=type)
    string = random.choice(list(generated_words)).string
    return {
        "string": string,
        "type": type,
        "definition": definition,
    }


async def get_random_definition_en() -> Tuple[str, str, str]:
    """
    Returns a random real word definition, type and example.
    """
    words = await RealWordEN.objects.all()
    word = random.choice(list(words))
    type, definition, example = await get_definition_en(word=word.string)
    while (not definition) or (type not in ALLOWED_TYPES_EN):
        print(
            f"Definition for word '{word}' or type '{type}' not supported, trying another word and definition..."
        )
        words = await RealWordEN.objects.all()
        word = random.choice(list(words))
        type, definition, example = await get_definition_en(word=word.string)
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
