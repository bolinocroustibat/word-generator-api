import math
import random
from typing import Tuple

import requests
from config import ALLOWED_TYPES, DICTIONNARY_EN_API_URL
from models import RealWordEN, GenereratedWordEN
from nltk import pos_tag
from nltk.tokenize import word_tokenize


async def generate_definition_en() -> str:
    type, definition, example = await get_random_definition_en()
    definition = await alter_definition_en(definition=definition, percentage=0.2)
    if type == "verb":
        generated_words = await GenereratedWordEN.objects.all(
            type=type, tense="infinitive"
        )
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
    while (not definition) or (type not in ALLOWED_TYPES):
        print(
            f"Definition for word '{word}' or type '{type}' not supported, trying another word and definition..."
        )
        words = await RealWordEN.objects.all()
        word = random.choice(list(words))
        type, definition, example = await get_definition_en(word=word.string)
    return type, definition, example


async def get_definition_en(word: str) -> Tuple[str, str, str]:
    """
    Returns the type and definition of a word using the dictionaryapi.
    """
    response = requests.get(f"{DICTIONNARY_EN_API_URL}{word}")
    try:
        meanings: list = response.json()[0]["meanings"]
    except:
        print(response.json())
        return None, None, None
    else:
        meaning: dict = random.choice(meanings)
        type: str = meaning["partOfSpeech"]
        definitions: list = meaning["definitions"]
        definition: str = random.choice(definitions)["definition"]
        example: str = random.choice(definitions).get("example", None)
        return type, definition, example


async def alter_definition_en(definition: str, percentage: float) -> str:
    """
    Alter a sentence randomly using NLTK POS tagging.
    See https://www.guru99.com/pos-tagging-chunking-nltk.html
    """
    POS_CORRESPONDANCE_EN = {
        "JJ": {"type": "adjective"},
        "JJR": {"type": "adjective"},
        "JJS": {"type": "adjective"},
        "RB": {"type": "adverb"},
        "RBR": {"type": "adverb"},
        "RBS": {"type": "adverb"},
        "NN": {"type": "noun", "number": "s"},
        "NNS": {"type": "noun", "number": "p"},
        "VB": {"type": "verb", "tense": "infinitive"},
        "VBG": {"type": "verb", "tense": "gerund"},
        "VBN": {"type": "verb", "tense": "past-participle"},
    }
    words = pos_tag(word_tokenize(definition))

    # List all the words with allowed types for replacement
    replacable_words = []
    for w in words:
        if w[1] in POS_CORRESPONDANCE_EN.keys():
            replacable_words.append(w)

    # Adjust the number of possible replacements
    k: int = math.ceil(len(replacable_words) * percentage)

    # Pick the words to replace
    to_replace: list[Tuple] = random.sample(replacable_words, k=k)

    # Replace the words
    for w in to_replace:
        type = POS_CORRESPONDANCE_EN[w[1]]["type"]
        if type == "noun":
            number = POS_CORRESPONDANCE_EN[w[1]]["number"]
            generated_words = await GenereratedWordEN.objects.all(
                type=type, number=number
            )
        elif type == "verb":
            tense = POS_CORRESPONDANCE_EN[w[1]]["tense"]
            generated_words = await GenereratedWordEN.objects.all(
                type=type, tense=tense
            )
        else:
            generated_words = await GenereratedWordEN.objects.all(type=type)
        replacement: str = random.choice(list(generated_words)).string
        print(f"Replacing '{w[0]}' with '{replacement}'...")
        definition = definition.replace(w[0], replacement)

    return definition