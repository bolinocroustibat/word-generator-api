import math
import random
from typing import Tuple

import spacy
from spacy.language import Language
from spacy_lefff import LefffLemmatizer, POSTagger
from tortoise.contrib.mysql.functions import Rand

from common.capitalize import capitalize, decapitalize
from models import GeneratedWordFR, RealWordFR


# Better tagger than the default Spacy POS tagger
# See https://github.com/sammous/spacy-lefff
@Language.factory("french_lemmatizer")
def create_french_lemmatizer(nlp, name):
    return LefffLemmatizer(after_melt=True, default=True)


@Language.factory("melt_tagger")
def create_melt_tagger(nlp, name):
    return POSTagger()


nlp = spacy.load("fr_core_news_sm")
nlp.add_pipe("melt_tagger", after="parser")
nlp.add_pipe("french_lemmatizer", after="melt_tagger")

POS_CORRESPONDANCE_FR = {
    # https://spacy.io/usage/linguistic-features
    "ADJ": {"type": "adjective"},
    # "ADP": {"type": "adposition"},
    "ADV": {"type": "adverb"},
    # "AUX": {"type": "auxiliary"},
    # "CCONJ": {"type": "coordinating conjunction"},
    # "DET": {"type": "determiner"},
    # "INTJ": {"type": "interjection"},
    "NOUN": {"type": "noun", "proper": False},
    # "NUM": {"type": "numeral"},
    # "PART": {"type": "particle"},
    # "PRON": {"type": "pronoun"},
    "PROPN": {"type": "noun", "proper": True},
    # "PUNCT": {"type": "punctuation"},
    # "SCONJ": {"type": "subordinating conjunction"},
    # "SYM": {"type": "symbol"},
    "VERB": {"type": "verb"},
    # "X": {"type": "other"},
}


async def alter_text_fr(text: str, percentage: float) -> str:
    """
    Alter a text randomly using Spacy and Lefff
    """
    
    text = decapitalize(text)
    
    replacable_words: list[dict] = list_replacable_words(text=text)
    # print(replacable_words)  # DEBUG

    # Adjust the number of possible replacements
    k: int = math.ceil(len(replacable_words) * percentage)
    # Pick the words to replace
    to_replace: list[dict] = random.sample(replacable_words, k=k)

    altered_text: str = await replace_words(text=text, to_replace=to_replace)

    return capitalize(altered_text)


def list_replacable_words(text: str) -> list[dict]:
    """
    Put all the words that can be replaced in a list with their characteristics
    """
    replacable_words = []
    tokens = nlp(text)
    for t in tokens:
        # print("=======")
        # print(t.text)
        # print(t.i)
        # print(t.pos_)
        # print(t.morph)
        # print("\n")
        if is_replacable(tokens=tokens, token=t):
            word_to_replace = {
                "string": t.text,
                "type": POS_CORRESPONDANCE_FR[t.pos_]["type"],
                "number": None,
                "gender": None,
                "tense": None,
                "conjug": None,
                "must_start_with_wowel": (
                    tokens[(t.i) - 1].text[-1] == "'" if tokens[(t.i) - 1] else False
                ), # TODO not being used yet
            }
            if t.pos_ in ["NOUN", "PROPN", "ADJ"]:
                if t.morph.get("Number"):
                    if t.morph.get("Number")[0] == "Sing":
                        word_to_replace["number"] = "s"
                    elif t.morph.get("Number")[0] == "Plur":
                        word_to_replace["number"] = "p"
                if t.morph.get("Gender"):
                    if t.morph.get("Gender")[0] == "Masc":
                        word_to_replace["gender"] = "m"
                    elif t.morph.get("Gender")[0] == "Fem":
                        word_to_replace["gender"] = "f"
                if t.pos_ == "PROPN":
                    word_to_replace["proper"] = True
                elif t.pos_ == "NOUN":
                    word_to_replace["proper"] = False
            elif t.pos_ == "VERB":
                if t.morph.get("Person"):
                    word_to_replace["conjug"] = int(t.morph.get("Person")[0])
                if t.morph.get("VerbForm"):
                    if t.morph.get("VerbForm")[0] == "Inf":
                        word_to_replace["tense"] = "infinitive"
                    elif t.morph.get("VerbForm")[0] == "Part":
                        if t.morph.get("Tense"):
                            if t.morph.get("Tense")[0] == "Past":
                                word_to_replace["tense"] = "past-participle"
                    elif t.morph.get("VerbForm")[0] == "Fin":
                        if t.morph.get("Tense"):
                            if t.morph.get("Tense")[0] == "Pres":
                                word_to_replace["tense"] = "present"
                            elif t.morph.get("Tense")[0] == "Past":
                                word_to_replace["tense"] = "past"
                            elif t.morph.get("Tense")[0] == "Fut":
                                word_to_replace["tense"] = "future"
            replacable_words.append(word_to_replace)
    # print(replacable_words)  # DEBUG
    return replacable_words


def is_replacable(tokens, token) -> bool:
    if (
        token.pos_ in POS_CORRESPONDANCE_FR.keys()
        and token.text[-1] not in ["'", "’"]
        and len(token.text) > 1
        and token.text not in ["pas"]
    ):
        return True
    return False


async def replace_words(text: str, to_replace: list[dict]) -> str:
    """
    Replace words in a text
    """
    for w in to_replace:
        if w["type"] == "noun":
            if not w["proper"]:
                generated_word = (
                    await GeneratedWordFR.filter(
                        type="noun",
                        number=w["number"],
                        gender=w["gender"],
                    )
                    .annotate(order=Rand())
                    .order_by("order")
                    .limit(1)
                )
            else:
                generated_word = (
                    await RealWordFR.filter(
                        type="noun", number=w["number"], gender=w["gender"], proper=True
                    )
                    .annotate(order=Rand())
                    .order_by("order")
                    .limit(1)
                )
        elif w["type"] == "adjective":
            generated_word = (
                await GeneratedWordFR.filter(
                    type="adjective",
                    number=w["number"],
                    gender=w["gender"],
                )
                .annotate(order=Rand())
                .order_by("order")
                .limit(1)
            )
        elif w["type"] == "verb":
            generated_word = (
                await GeneratedWordFR.filter(
                    type="verb", tense=w["tense"], conjug=w["conjug"]
                )
                .annotate(order=Rand())
                .order_by("order")
                .limit(1)
            )
        else:
            generated_word = (
                await GeneratedWordFR.filter(type=w["type"])
                .annotate(order=Rand())
                .order_by("order")
                .limit(1)
            )
        if generated_word:
            replacement: str = generated_word[0].string
            print("Replacing '{}' with '{}'...".format(w["string"], replacement))
            if w["string"].istitle():
                text = text.replace(w["string"], replacement.title())
            else:
                text = text.replace(w["string"], replacement)
        else:
            print(f"Couldn't find any replacement for '{w}'.")

    return text
