import json
import random
from datetime import datetime

from tortoise.exceptions import IntegrityError

from common.real_word import if_real_exists
from en.classify import classify_en
from fr.classify import classify_fr
from models import GeneratedWordEN, GeneratedWordFR


async def generate_word_and_save(lang: str, ip: str) -> dict | None:
    already_generated = True  # assume it has already been generated so we enter the while loop at least once  # noqa: E501
    retries = 0
    while already_generated and retries < 10:
        try:
            string: str = await generate_word(lang=lang, must_not_be_real=True)
            response: dict = {"string": string}
            if lang == "en":
                word_classes: dict = classify_en(word=string)
                await GeneratedWordEN.create(
                    string=string,
                    type=word_classes["type"],
                    number=word_classes["number"],
                    tense=word_classes["tense"],
                    date=datetime.utcnow(),
                    ip=ip,
                )
                response.update(word_classes)
            if lang == "fr":
                word_classes: dict = classify_fr(word=string)
                await GeneratedWordFR.create(
                    string=string,
                    type=word_classes["type"],
                    gender=word_classes["gender"],
                    number=word_classes["number"],
                    tense=word_classes["tense"],
                    conjug=word_classes["conjug"],
                    date=datetime.utcnow(),
                    ip=ip,
                )
                response.update(word_classes)
            return response
        except IntegrityError:
            print(f"Generated word '{string}' was already generated. Retrying...")
            already_generated = True
        retries += 1
    return None


async def generate_word(lang: str, must_not_be_real: bool = True) -> str:
    """
    Generate a word, by retrying the algorithm if:
    - the generated word is too long (max 13 chars)
    - the generated word is too short (min 3 chars)
    - the generated word already exists in the dictionnary (optional)
    Try only 5 times, if not possible, will return the word generated before.
    """
    json_proba_file = f"{lang}/data/proba_table_2char_{lang.upper()}.json"

    generated_word = _generate_word_core(json_proba_file=json_proba_file)
    real_exists = False
    if must_not_be_real:
        real_exists = await if_real_exists(lang=lang, string=generated_word)

    i = 0
    while (len(generated_word) < 3) or (len(generated_word) > 13) or real_exists:
        print(f"Generated word '{generated_word}' not acceptable. Retrying...")
        generated_word = _generate_word_core(json_proba_file=json_proba_file)
        real_exists = False
        if must_not_be_real:
            real_exists = await if_real_exists(lang=lang, string=generated_word)
        i += 1
        if i > 10:
            break

    return generated_word


def _generate_word_core(json_proba_file: str) -> str:
    """
    Generate a word that don't exist, based on the characters probability table,
    depending on each language.
    """
    with open(json_proba_file, "r") as file:
        probas: dict = json.load(file)
    char1 = random.choices(
        list(probas["first_letter"].keys()),
        weights=list(probas["first_letter"].values()),
        k=1,
    )[0]
    word = char1
    # for _ in probas[char1]:
    # choose second char
    char2 = random.choices(
        list(probas[char1].keys()), weights=list(probas[char1].values()), k=1
    )[0]
    if char2 == "last_letter":
        # it's a 1-letter word
        return word
    # it's more than a 1-letter
    word = word + char2
    # now loop for other chars
    for i in range(0, 25):
        chosen_char = random.choices(
            list(probas[char1 + char2].keys()),
            weights=list(probas[char1 + char2].values()),
            k=1,
        )[0]
        if chosen_char == "last_letter":
            return word
        else:
            word = word + chosen_char
            char1 = char2
            char2 = chosen_char
    return word
