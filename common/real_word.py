from models import Language, RealWord


async def if_real_exists(lang: str, string: str) -> bool:
    """
    Check if the word exists among real dictionary words
    """
    # Get language ID
    language = await Language.get(code=lang)

    if lang == "en":
        real_words = await RealWord.filter(language=language, string=string.lower())
        possible_duplicates = set()
        for w in real_words:
            possible_duplicates.add(w.string)
            if w.type == "noun" and w.number == "s":
                possible_duplicates.add(w.string + "s")
        if string.lower() in [w.lower() for w in possible_duplicates]:
            print(f"Word '{string}' already exists in English dictionary.")
            return True
    elif lang == "fr":
        real_words = await RealWord.filter(language=language, string=string)
        if string.lower() in [w.string.lower() for w in real_words]:
            print(f"Word '{string}' already exists in French dictionary.")
            return True
    else:
        # For other languages, check against dictionary file
        dictionary = []
        with open(f"{lang}/data/dictionary_{lang.upper()}.txt", "r") as dictionary_file:
            for word in dictionary_file:
                dictionary.append(word.strip())
        if string in dictionary:
            print(f"Word '{string}' already exists in {lang} dictionary.")
            return True
    return False
