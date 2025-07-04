import os
from datetime import UTC, datetime

import requests
from dotenv import load_dotenv
from tortoise.contrib.postgres.functions import Random

from common import decapitalize
from models import GeneratedDefinition, GeneratedWord, Language, RealWord

from .alter_text import alter_text_fr

load_dotenv()

ALLOWED_TYPES_FR = {"nom": "noun", "ver": "verb", "adj": "adjective", "adv": "adverb"}
DICTIONNARY_FR_API_URL = "https://api.dicolink.com/v1/mot/"
DICTIONNARY_FR_API_KEY = os.getenv("DICTIONNARY_FR_API_KEY")


async def generate_definition_fr(percentage: float, ip: str | None = None) -> dict:
    random_definition = await get_random_definition_fr()
    real_string = random_definition["real_string"]
    type = random_definition["type"]
    gender = random_definition["gender"]
    definition = random_definition["definition"]

    # Get French language ID
    french = await Language.get(code="fr")

    if type == "verb":
        generated_word = (
            await GeneratedWord.filter(language=french, type=type, tense="infinitive")
            .annotate(order=Random())
            .order_by("order")
            .limit(1)
        )
    elif type == "noun":
        generated_word = (
            await GeneratedWord.filter(language=french, type=type, number="s", gender=gender)
            .annotate(order=Random())
            .order_by("order")
            .limit(1)
        )
    else:
        generated_word = (
            await GeneratedWord.filter(language=french, type=type, number="s", gender=gender)
            .annotate(order=Random())
            .order_by("order")
            .limit(1)
        )

    if not generated_word:
        raise ValueError(f"No generated word found for type {type}")

    generated_string: str = generated_word[0].string
    definition = await alter_text_fr(
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
        "gender": gender,
        "definition": definition,
    }


async def get_random_definition_fr() -> dict:
    """
    Returns a random real word definition with its associated type and gender.
    """
    count = 0
    definition = None
    real_string: str | None = None
    type: str | None = None
    gender: str | None = None

    # Get French language ID
    french = await Language.get(code="fr")

    while (not definition) or (type not in ALLOWED_TYPES_FR.values()):
        if count > 0:
            print(
                f"Definition for word '{real_string}' or type '{type}' not "
                "supported, trying another word and definition..."
            )
        # Get a random real word
        word = (
            await RealWord.filter(
                language=french,
                type__in=list(ALLOWED_TYPES_FR.values()),
                proper=False,
                complex__not=True,
            )
            .annotate(order=Random())
            .order_by("order")
            .limit(1)
        )

        if not word:
            print("No real words found in database")
            count += 1
            continue

        # If it's a feminine adjective, we need to get a masculine adjective instead
        if word[0].type == "adjective" and word[0].gender == "f":
            word = (
                await RealWord.filter(
                    language=french,
                    type="adjective",
                    gender="m",
                    proper=False,
                    complex__not=True,
                )
                .annotate(order=Random())
                .order_by("order")
                .limit(1)
            )

            if not word:
                print("No masculine adjective found")
                count += 1
                continue

        real_string = word[0].string
        gender = word[0].gender

        if real_string:
            definition_dict: dict = await get_definition_from_word_fr(word=real_string)
            type = definition_dict["type"]
            definition = definition_dict["definition"]

        count += 1

    return {
        "real_string": real_string,
        "type": type,
        "gender": gender,
        "definition": definition,
    }


async def get_definition_from_word_fr(word: str) -> dict:
    """
    Returns the type and definition of a given word using the French Dicolink API.
    """
    type: str | None = None
    definition: str | None = None

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
        if type:
            type = ALLOWED_TYPES_FR.get(type, "unknown")
        else:
            type = "unknown"

    return {
        "type": type,
        "definition": decapitalize(definition) if definition else None,
    }
