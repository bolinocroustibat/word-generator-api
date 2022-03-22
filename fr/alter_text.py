import math
import random
from typing import Tuple

from nltk.tokenize import word_tokenize
from treetagger import TreeTagger
from tortoise.contrib.mysql.functions import Rand

from .classify import classify_fr
from models import GeneratedWordFR


tt_fr = TreeTagger(language="french")


async def alter_text_fr(text: str, percentage: float) -> str:
    """
    Alter a text randomly using TreeTagger French POS tagging.
    See https://www.cis.lmu.de/~schmid/tools/TreeTagger/data/french-tagset.html
    """
    POS_CORRESPONDANCE_FR = {
        "ADJ": {"type": "adjective"},
        "ADV": {"type": "adverb"},
        "NOM": {"type": "noun"},
        "VER:infi": {"type": "verb", "tense": "infinitive"},
        "VER:futu": {"type": "verb", "tense": "future"},
        "VER:pres": {"type": "verb", "tense": "present"},
        "VER:simp": {"type": "verb", "tense": "past"},
        "VER:pper": {"type": "verb", "tense": "past-participle"},
    }
    tags = tt_fr.tag(word_tokenize(text))

    # List all the words with allowed types for replacement
    replacable_words = []
    for t in tags:
        if t[1] in POS_CORRESPONDANCE_FR.keys():
            word_class = classify_fr(word=t[0])
            if word_class["type"] == POS_CORRESPONDANCE_FR[t[1]]["type"]:
                if word_class["type"] in ["noun", "adjective"]:
                    # We agree on type. We can maybe trust the number from manual classification.
                    word_to_replace = {
                        "string": t[0],
                        "type": word_class["type"],
                        "number": word_class["number"],
                        "gender": word_class["gender"],
                    }
                    replacable_words.append(word_to_replace)
                elif word_class["type"] == "verb":
                    if word_class["tense"] == POS_CORRESPONDANCE_FR[t[1]]["tense"]:
                        # We agree on verb tense. We can trust the conjugation from manual classification.
                        word_to_replace = {
                            "string": t[0],
                            "type": word_class["type"],
                            "tense": word_class["tense"],
                            "conjug": word_class["conjug"],
                        }
                        replacable_words.append(word_to_replace)
                    else:
                        print(
                            "Verb disagreement on the tense of '{}': POS says it's {}, but manual classification says it's {}.".format(
                                t[0],
                                POS_CORRESPONDANCE_FR[t[1]]["tense"],
                                word_class["tense"],
                            )
                        )
            else:
                print(
                    "Disagreement on '{}': POS says it's {}, but manual classification says it's {}.".format(
                        t[0], POS_CORRESPONDANCE_FR[t[1]]["type"], word_class["type"]
                    )
                )

    # Adjust the number of possible replacements
    k: int = math.ceil(len(replacable_words) * percentage)

    # Pick the words to replace
    to_replace: list[Tuple] = random.sample(replacable_words, k=k)

    # Replace the words
    for w in to_replace:
        if w["type"] in ["noun", "adjective"]:
            generated_word = (
                await GeneratedWordFR.filter(
                    type=w["type"], number=w["number"], gender=w["gender"]
                )
                .annotate(order=Rand())
                .order_by("order")
                .limit(1)
            )
        elif w["type"] == "verb":
            generated_word = (
                await GeneratedWordFR.filter(
                    type=w["type"], tense=w["tense"], conjug=w["conjug"]
                )
                .annotate(order=Rand())
                .order_by("order")
                .limit(1)
            )
        else:
            generated_word = (
                await GeneratedWordFR.filter(type == w["type"])
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
