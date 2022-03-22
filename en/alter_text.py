import math
import random
from typing import Tuple

from nltk import pos_tag
from nltk.tokenize import word_tokenize

from models import GenereratedWordEN


async def alter_text_en(text: str, percentage: float) -> str:
    """
    Alter a text randomly using NLTK POS tagging.
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
    words = pos_tag(word_tokenize(text))

    # List all the words with allowed types for replacement
    replacable_words = []
    for w in words:
        if w[1] in POS_CORRESPONDANCE_EN.keys():
            replacable_words.append(w)

    # Adjust the number of possible replacements
    k: int = math.ceil(len(replacable_words) * percentage)

    # Pick the words to replace
    to_replace: list[Tuple] = random.sample(replacable_words, k=k)

    # Replace the words in the text
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
        if w[0].istitle():
            text = text.replace(w[0], replacement.title())
        else:
            text = text.replace(w[0], replacement)

    return text
