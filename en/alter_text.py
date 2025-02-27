import math
import random

from nltk import pos_tag
from nltk.tokenize import word_tokenize
from tortoise.contrib.postgres.functions import Random

from models import GeneratedWord, Language

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


async def alter_text_en(
    text: str, percentage: float, forced_replacements: dict | None = None
) -> str:
    """
    Alter a text randomly using NLTK POS tagging.
    See https://www.guru99.com/pos-tagging-chunking-nltk.html
    """
    forced_replacements = forced_replacements or {}
    replacable_words: list[dict] = list_replacable_words(
        text=text, not_to_replace=list(forced_replacements.keys())
    )

    # Adjust the number of possible replacements
    k: int = math.ceil(len(replacable_words) * percentage)
    # Pick the words to replace
    to_replace: list[dict] = random.sample(replacable_words, k=k)

    # Replace the forced replacements
    if forced_replacements:
        for k, v in forced_replacements.items():
            print(f"Force-replacing '{k}' with '{v}'...")
            if k.istitle():
                text = text.replace(k, v.title())
            else:
                text = text.replace(k, v)

    altered_text: str = await replace_words(text=text, to_replace=to_replace)

    return altered_text


def list_replacable_words(text: str, not_to_replace: list[str]) -> list[dict]:
    """
    Put all the words that can be replaced in a list with their types
    """
    words = pos_tag(word_tokenize(text))
    replacable_words = []
    for w in words:
        if w[1] in POS_CORRESPONDANCE_EN.keys() and w[0] not in not_to_replace:
            word_to_replace = POS_CORRESPONDANCE_EN[w[1]]
            word_to_replace["string"] = w[0]
            if word_to_replace not in replacable_words:
                replacable_words.append(word_to_replace)
    return replacable_words


async def replace_words(text: str, to_replace: list[dict]) -> str:
    # Get English language ID
    english = await Language.get(code="en")

    # Replace the words in the text
    for w in to_replace:
        if w["type"] == "noun":
            generated_word = (
                await GeneratedWord.filter(language=english, type="noun", number=w["number"])
                .annotate(order=Random())
                .order_by("order")
                .limit(1)
            )
        elif w["type"] == "verb":
            generated_word = (
                await GeneratedWord.filter(language=english, type="verb", tense=w["tense"])
                .annotate(order=Random())
                .order_by("order")
                .limit(1)
            )
        else:
            generated_word = (
                await GeneratedWord.filter(language=english, type=w["type"])
                .annotate(order=Random())
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
