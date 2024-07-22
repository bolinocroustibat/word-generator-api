def classify_fr(word: str) -> dict:
    """
    Classify French word
    """
    type = None
    gender = None
    number = None
    tense = None
    conjug = None
    if word[-5:] == "aient":
        type = "verb"
        tense = "past"
        conjug = "6"
    elif word[-5:] == "iques":
        type = "adjective"
        gender = "m"
        number = "p"
    elif word[-5:] == "euses":
        type = "adjective"
        gender = "f"
        number = "p"
    elif (word[-4:] == "ment") and (
        get_char_from_position(word, -5) in ["a", "e", "é", "i", "î", "ï", "o", "ô", "u", "û"]
    ):
        type = "adverb"
    elif word[-4:] == "ique":
        type = "adjective"
        gender = "m"
        number = "s"
    elif word[-4:] == "euse":
        type = "adjective"
        gender = "f"
        number = "p"
    elif word[-4:] == "ives":
        type = "adjective"
        gender = "f"
        number = "p"
    elif word[-3:] == "ées":
        type = "verb"
        tense = "past-participle"
        gender = "f"
        number = "p"
    elif word[-3:] == "ons":
        type = "verb"
        tense = "present"
        conjug = "4"
    elif word[-3:] == "ent":
        type = "verb"
        tense = "present"
        conjug = "6"
    elif word[-3:] == "ais":
        type = "verb"
        tense = "past"
        conjug = "1"
    elif word[-3:] == "ait":
        type = "verb"
        tense = "past"
        conjug = "3"
    elif word[-3:] == "ras":
        type = "verb"
        tense = "future"
        conjug = "2"
    elif word[-3:] == "ont":
        type = "verb"
        tense = "future"
        conjug = "6"
    elif word[-3:] == "ive":
        type = "adjective"
        gender = "f"
        number = "s"
    elif word[-3:] in ["eux", "ifs"]:
        type = "adjective"
        gender = "m"
        number = "p"
    elif word[-2:] == "ra":
        type = "verb"
        tense = "future"
        conjug = "1"
    elif word[-2:] == "ai" and (get_char_from_position(word, -3) == "r"):
        type = "verb"
        tense = "future"
        conjug = "1"
    elif word[-2:] == "ai" and (get_char_from_position(word, -3) != "r"):
        type = "verb"
        tense = "past"
        conjug = "1"
    elif word[-2:] == "as":
        type = "verb"
        tense = "present"
        conjug = "2"
    elif word[-2:] == "ez":
        type = "verb"
        tense = "present"
        conjug = "5"
    elif word[-2:] == "if":
        type = "adjective"
        gender = "m"
        number = "s"
    elif word[-2:] == "es":
        type = "noun"
        gender = "f"
        number = "p"
    elif word[-2:] == "ée":
        type = "verb"
        tense = "past-participle"
        gender = "f"
        number = "s"
    elif word[-2:] == "és":
        type = "verb"
        tense = "past-participle"
        gender = "m"
        number = "p"
    elif word[-2:] in ["er", "ir"]:
        type = "verb"
        tense = "infinitive"
    elif word[-1:] == "e":
        type = "noun"
        gender = "f"
        number = "s"
    elif word[-1:] == "é":
        type = "verb"
        tense = "past-participle"
        gender = "m"
        number = "s"
    elif word[-1:] == "s":
        type = "noun"
        gender = "m"
        number = "p"
    else:
        type = "noun"
        gender = "m"
        number = "s"

    return {
        "type": type,
        "gender": gender,
        "number": number,
        "tense": tense,
        "conjug": conjug,
    }


def get_char_from_position(word: str, position: int) -> str | None:
    try:
        return word[position]
    except Exception:
        return None
