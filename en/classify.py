from typing import Tuple


def classify_en(word: str) -> dict:
    """
    Classify English word
    """
    type = None
    number = None
    tense = None
    if word[-6:] == "nesses":
        type = "noun"
        number = "p"
    elif word[-5:] in ["ances", "ences", "ships", "ments"]:
        type = "noun"
        number = "p"
    elif word[-4:] in ["ance", "ence", "ness", "ship", "ment"]:
        type = "noun"
        number = "s"
    elif word[-4:] == "ities":
        type = "noun"
        number = "p"
    elif word[-4:] in ["able", "ible", "less"]:
        type = "adjective"
    elif word[-4:] == "ions":
        type = "noun"
        number = "p"
    elif word[-3:] in ["ity", "ion"]:
        type = "noun"
        number = "s"
    elif word[-3:] in ["ers", "ars", "ors"]:
        type = "noun"
        number = "p"
    elif word[-3:] in ["our", "ish", "ful", "ant", "ent", "ive", "ous"]:
        type = "adjective"
    elif word[-3:] in ["ate", "ify", "ise", "ize"]:
        type = "verb"
        tense = "infinitive"
    elif word[-3:] == "ing":
        type = "verb"
        tense = "gerund"
    elif word[-2:] in ["er", "ar", "or"]:
        type = "noun"
        number = "s"
    elif word[-2:] in ["ic", "al"]:
        type = "adjective"
    elif word[-2:] == "ly":
        type = "adverb"
    elif word[-2:] == "en":
        type = "verb"
        number = "infinitive"
    elif word[-2:] == "ed":
        type = "verb"
        number = "past-participle"
    elif word[-1:] == "y":
        type = "adjective"
    elif word[-1:] == "s":
        type = "noun"
        number = "p"
    else:
        type = "noun"
        number = "s"
    return {
        "type": type,
        "number": number,
        "tense": tense,
    }
