from config import TRANSLATIONS_FR
from fr.generate_definition import generate_definition_fr


async def generate_tweet_fr() -> str:
    generated: dict = await generate_definition_fr(percentage=0.6)
    string: str = generated["string"].capitalize()
    type_en: str = generated["type"]
    type_fr = TRANSLATIONS_FR[type_en]
    gender: str = generated["gender"]
    definition: str = generated["definition"]
    if gender:
        gender_fr = TRANSLATIONS_FR[gender]
        return f"{string} ({type_fr} {gender_fr}) : {definition}"
    return f"{string} ({type_fr}) : {definition}"
