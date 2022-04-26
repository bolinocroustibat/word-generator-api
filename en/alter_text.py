import math
import random

from nltk import pos_tag
from nltk.tokenize import word_tokenize
from tortoise.contrib.mysql.functions import Rand

from models import GeneratedWordEN

POS_CORRESPONDANCE_EN = {
    # See https://www.guru99.com/pos-tagging-chunking-nltk.html
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


async def alter_text_en(text: str, percentage: float) -> str:
    """
    Alter a text randomly using NLTK POS tagging.
    See https://www.guru99.com/pos-tagging-chunking-nltk.html
    """

    replacable_words: list[dict] = list_replacable_words(text=text)

    # Adjust the number of possible replacements
    k: int = math.ceil(len(replacable_words) * percentage)
    # Pick the words to replace
    to_replace: list[dict] = random.sample(replacable_words, k=k)

    altered_text: str = await replace_words(text=text, to_replace=to_replace)

    return altered_text


def list_replacable_words(text: str) -> list[dict]:
    """
    Put all the words that can be replaced in a list with their types
    """
    words = pos_tag(word_tokenize(text))
    replacable_words = []
    for w in words:
        if w[1] in POS_CORRESPONDANCE_EN.keys():
            word_to_replace = POS_CORRESPONDANCE_EN[w[1]]
            word_to_replace["string"] = w[0]
            if word_to_replace not in replacable_words:
                replacable_words.append(word_to_replace)
    return replacable_words


async def replace_words(text: str, to_replace: list[dict]) -> str:
    # Replace the words in the text
    for w in to_replace:
        if w["type"] == "noun":
            generated_word = (
                await GeneratedWordEN.filter(type="noun", number=w["number"])
                .annotate(order=Rand())
                .order_by("order")
                .limit(1)
            )
        elif w["type"] == "verb":
            generated_word = (
                await GeneratedWordEN.filter(type="verb", tense=w["tense"])
                .annotate(order=Rand())
                .order_by("order")
                .limit(1)
            )
        else:
            generated_word = (
                await GeneratedWordEN.filter(type=w["type"])
                .annotate(order=Rand())
                .order_by("order")
                .limit(1)
            )
        replacement: str = generated_word[0].string
        print("Replacing '{}' with '{}'...".format(w["string"], replacement))
        if w["string"].istitle():
            text = text.replace(w["string"], replacement.title())
        else:
            text = text.replace(w["string"], replacement)
    return text
