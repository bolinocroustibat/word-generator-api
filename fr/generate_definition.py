from typing import Optional

import requests
from tortoise.contrib.mysql.functions import Rand

from common import decapitalize
from config import ALLOWED_TYPES_FR, DICTIONNARY_FR_API_KEY, DICTIONNARY_FR_API_URL
from fr.alter_text import alter_text_fr
from models import GeneratedWordFR, RealWordFR


async def generate_definition_fr(percentage: float) -> dict:

    random_definition = await get_random_definition_fr()
    real_string = random_definition["real_string"]
    type = random_definition["type"]
    gender = random_definition["gender"]
    definition = random_definition["definition"]

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
    generated_string: str = generated_word[0].string
    definition = await alter_text_fr(
        text=definition,
        percentage=percentage,
        forced_replacements={real_string: generated_string},
    )
    return {
        "string": generated_string,
        "type": type,
        "gender": gender,
        "definition": definition,
    }


async def get_random_definition_fr() -> dict:
    """
    Returns a random real word definition with its associated type and gender.
    """
    count = 0
    definition = None
    real_string: Optional[str] = None
    type: Optional[str] = None
    gender: Optional[str] = None

    while (not definition) or (type not in ALLOWED_TYPES_FR.values()):
        if count > 0:
            print(
                f"Definition for word '{real_string}' or type '{type}' not "
                "supported, trying another word and definition..."
            )
        # Get a random real word
        word = (
            await RealWordFR.filter(
                type__in=ALLOWED_TYPES_FR.values(),
                proper=0,
                complex__not=1,
            )
            .annotate(order=Rand())
            .order_by("order")
            .limit(1)
        )
        # If it's a feminine adjective, we need to get a masculine adjective instead
        if (word[0].type == "adjective") and (word[0].gender == "f"):
            word = (
                await RealWordFR.filter(
                    type="adjective",
                    gender="m",
                    proper=0,
                    complex__not=1,
                )
                .annotate(order=Rand())
                .order_by("order")
                .limit(1)
            )
        real_string = word[0].string
        gender = word[0].gender

        definition_dict: dict = await get_definition_fr(word=real_string)
        type = definition_dict["type"]
        definition = definition_dict["definition"]

        count += 1

    return {
        "real_string": real_string,
        "type": type,
        "gender": gender,
        "definition": definition,
    }


async def get_definition_fr(word: str) -> dict:
    """
    Returns the type and definition of a given word using the French Dicolink API.
    """
    type: Optional[str] = None
    definition: Optional[str] = None

    response = requests.get(
        f"{DICTIONNARY_FR_API_URL}{word}/definitions?limite=1&api_key={DICTIONNARY_FR_API_KEY}"
    )

    try:
        res = response.json()[0]
        type = res["nature"].split()[0]
        definition = res["definition"].strip()
    except Exception:
        print(f"Dicolink API error: {str(response)}")
    else:
        print(res)  # TODO: to remove, it's for debug
        type = ALLOWED_TYPES_FR.get(type, "unknown")

    return {
        "type": type,
        "definition": decapitalize(definition) if definition else None,
    }
