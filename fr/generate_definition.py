from typing import Tuple

import requests
from tortoise.contrib.mysql.functions import Rand

from config import ALLOWED_TYPES_FR, DICTIONNARY_FR_API_KEY, DICTIONNARY_FR_API_URL
from models import GeneratedWordFR, RealWordFR
from fr.alter_text import alter_text_fr


async def generate_definition_fr(percentage: float) -> str:
    type, gender, definition = await get_random_definition_fr()
    definition = await alter_text_fr(text=definition, percentage=percentage)
    if type == "verb":
        generated_word = (
            await GeneratedWordFR.filter(type=type, tense="infinitive")
            .annotate(order=Rand())
            .order_by("order")
            .limit(1)
        )
    elif type == "noun":
        generated_word = (
            await GeneratedWordFR.filter(type=type, number="s", gender=gender)
            .annotate(order=Rand())
            .order_by("order")
            .limit(1)
        )
    else:
        generated_word = (
            await GeneratedWordFR.filter(type=type, number="s", gender=gender)
            .annotate(order=Rand())
            .order_by("order")
            .limit(1)
        )
    return {
        "string": generated_word[0].string,
        "type": type,
        "gender": gender,
        "definition": definition,
    }


async def get_random_definition_fr() -> Tuple[str, str, str]:
    """
    Returns a random real word definition, and type.
    """
    # word = await RealWordFR.objects.order_by("?").limit(1).all(type__in=ALLOWED_TYPES_FR.values(), conjug__isnull=True, proper=0, complex=0)
    word = (
        await RealWordFR.filter(
            type__in=ALLOWED_TYPES_FR.values(),
            proper=0,
            complex=0,
        )
        .annotate(order=Rand())
        .order_by("order")
        .limit(1)
    )
    gender = word[0].gender
    type, definition = await get_definition_fr(word=word[0].string)
    while (not definition) or (type not in ALLOWED_TYPES_FR.values()):
        print(
            f"Definition for word '{word[0]}' or type '{type}' not supported, trying another word and definition..."
        )
        word = (
            await RealWordFR.filter(
                type__in=ALLOWED_TYPES_FR.values(),
                proper=0,
                complex=0,
            )
            .annotate(order=Rand())
            .order_by("order")
            .limit(1)
        )
        gender = word[0].gender
        type, definition = await get_definition_fr(word=word[0].string)
    return type, gender, definition


async def get_definition_fr(word: str) -> Tuple[str, str]:
    """
    Returns the type and definition of a given word using the French Dicolink API.
    """
    response = requests.get(
        f"{DICTIONNARY_FR_API_URL}{word}/definitions?limite=1&api_key={DICTIONNARY_FR_API_KEY}"
    )
    try:
        res: dict = response.json()[0]
        type: str = res["nature"].split()[0]
        definition: str = res["definition"].strip()
    except:
        print(f"Dicolink API error: {str(response)}")
        return None, None
    else:
        print(res)  # TODO: to remove, it's for debug
        type = ALLOWED_TYPES_FR.get(type, "unknown")
        return type, definition