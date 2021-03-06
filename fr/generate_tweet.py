from fr.generate_definition import generate_definition_fr

TRANSLATIONS_FR = {
    "adjective": "adjectif",
    "adv": "adverbe",
    "verb": "verbe",
    "noun": "nom",
    "f": "féminin",
    "m": "masculin",
}


async def generate_tweet_fr() -> str:
    generated: dict = await generate_definition_fr(percentage=0.6)
    string: str = generated["string"].capitalize()
    type_en: str = generated["type"]
    type_fr = TRANSLATIONS_FR[type_en]
    definition: str = generated["definition"]
    if type_en == "noun":
        gender_fr = TRANSLATIONS_FR[generated["gender"]]
        return f"{string} ({type_fr} {gender_fr}) : {definition}"
    return f"{string} ({type_fr}) : {definition}"
