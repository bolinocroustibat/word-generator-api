import math
import random

import spacy
from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc, Token
from spacy_lefff import LefffLemmatizer, POSTagger
from tortoise.contrib.postgres.functions import Random

from common import decapitalize
from models import GeneratedWordFR, RealWordFR

from .correct_text import add_to_text_fr, correct_text_fr


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
Token.set_extension("replacement", default=None)
Token.set_extension("type", default=None)
Token.set_extension("number", default=None)
Token.set_extension("gender", default=None)
Token.set_extension("tense", default=None)
Token.set_extension("conjug", default=None)


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


async def alter_text_fr(text: str, percentage: float, forced_replacements: dict | None = {}) -> str:
    """
    Alter a text randomly using Spacy and Lefff
    """
    text = decapitalize(text)

    # Split into tokens/words
    doc: Doc = nlp(text)

    # Adjust the number of possible replacements
    replaceable_t_ids: list = get_replacable_tokens_ids(
        doc=doc, not_to_replace=list(forced_replacements.keys())
    )
    k: int = math.ceil(len(replaceable_t_ids) * percentage)
    # Pick the tokens to replace
    tokens_ids_to_replace: list = random.sample(replaceable_t_ids, k=k)
    # Add the replacements to the tokens
    doc = await replace_tokens(
        doc=doc,
        tokens_ids_to_replace=tokens_ids_to_replace,
        forced_replacements=forced_replacements,
    )

    # Build back the text from the tokens and their replacements
    altered_text = ""
    for t in doc:
        if t._.replacement:
            altered_text = add_to_text_fr(altered_text, t._.replacement)
        else:
            altered_text = add_to_text_fr(altered_text, t.text)

    return correct_text_fr(altered_text)


def get_replacable_tokens_ids(doc: Doc, not_to_replace: list[str]) -> list[int]:
    """
    Tag all the tokens that can be replaced
    """
    replaceable_t_ids = []
    for t in doc:
        if (
            t.pos_ in POS_CORRESPONDANCE_FR.keys()
            and len(t.text) > 1
            and t.text not in not_to_replace
            and t.text[-1] not in ["'", "’"]
            and t.text not in ["pas"]
        ):
            replaceable_t_ids.append(t.i)
    return replaceable_t_ids


async def replace_tokens(
    doc: Doc, tokens_ids_to_replace: list, forced_replacements: dict | None
) -> Doc:
    """
    Replace the tokens in the doc
    """
    for t in doc:
        if t.text in forced_replacements.keys():
            t._.replacement = forced_replacements[t.text]
            print("Force-replacing '{}' with '{}'...".format(t.text, t._.replacement))
        if t.i in tokens_ids_to_replace and not t._.replacement:
            # Tag the token by adding some extensions need for the DB select
            t = tag_token(t)
            if t.pos_ == "PROPN":
                replacement = (
                    await RealWordFR.filter(
                        type="noun", number=t._.number, gender=t._.gender, proper=True
                    )
                    .annotate(order=Random())
                    .order_by("order")
                    .limit(1)
                )
            elif t.pos_ in ["NOUN", "ADJ", "VERB", "ADV"]:
                replacement = (
                    await GeneratedWordFR.filter(
                        type=t._.type[0],  # This custom extension is set as a tuple...
                        # ...instead of a string. No idea why!
                        number=t._.number,
                        gender=t._.gender,
                        tense=t._.tense,
                        conjug=t._.conjug,
                    )
                    .annotate(order=Random())
                    .order_by("order")
                    .limit(1)
                )
            if replacement:
                if t.text.istitle():
                    t._.replacement = replacement[0].string.title()
                else:
                    t._.replacement = replacement[0].string
                print(
                    "Replacing '{}' ({} {} {}) with '{}'...".format(
                        t.text, t._.type[0], t._.gender, t._.number, t._.replacement
                    )
                )
                matcher = Matcher(nlp.vocab)
                matcher.add("pattern1", [[{"LOWER": t.text}]])
                matches = matcher(doc)
                for _, pos, _ in matches:
                    doc[pos]._.replacement = t._.replacement
                    replace_pronoun(doc=doc, pos=pos)
            else:
                print("Couldn't find any replacement for '{}'.".format(t.text))

    return doc


def tag_token(t: Token) -> Token:
    """ """
    t._.type = (POS_CORRESPONDANCE_FR[t.pos_]["type"],)
    if t.morph.get("Number"):
        if t.morph.get("Number")[0] == "Sing":
            t._.number = "s"
        elif t.morph.get("Number")[0] == "Plur":
            t._.number = "p"
    if t.morph.get("Gender"):
        if t.morph.get("Gender")[0] == "Masc":
            t._.gender = "m"
        elif t.morph.get("Gender")[0] == "Fem":
            t._.gender = "f"
    if t.morph.get("Person"):
        t._.conjug = int(t.morph.get("Person")[0])
    if t.morph.get("VerbForm"):
        if t.morph.get("VerbForm")[0] == "Inf":
            t._.tense = "infinitive"
        elif t.morph.get("VerbForm")[0] == "Part":
            if t.morph.get("Tense"):
                if t.morph.get("Tense")[0] == "Past":
                    t._.tense = "past-participle"
        elif t.morph.get("VerbForm")[0] == "Fin":
            if t.morph.get("Tense"):
                if t.morph.get("Tense")[0] == "Pres":
                    t._.tense = "present"
                elif t.morph.get("Tense")[0] == "Past":
                    t._.tense = "past"
                elif t.morph.get("Tense")[0] == "Fut":
                    t._.tense = "future"
    return t


def replace_pronoun(doc: Doc, pos: int):
    VOWELS = ["a", "à", "e", "é", "è", "ê", "i", "î", "ï", "o", "ô", "u", "ù", "y"]
    token = doc[pos]
    previous_token = doc[pos - 1]
    if previous_token.text[-1] in ["'", "’"] and token._.replacement[0] not in VOWELS:
        print(
            'Replacing pronoun "{}" before "{}" (position {}) to match with replacement "{}"...'.format(
                previous_token, doc[pos].text, pos, token._.replacement
            )
        )
        if previous_token.pos_ == "ADP":
            doc[pos - 1]._.replacement = "de"
        elif previous_token.pos_ == "DET":
            doc[pos - 1]._.replacement = "le"
            try:
                if doc[pos].morph.get("Gender")[0] == "Fem":
                    doc[pos - 1]._.replacement = "la"
            except IndexError:
                pass
