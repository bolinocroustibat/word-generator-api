from models import RealWordEN, RealWordFR


async def if_real_exists(lang: str, string: str) -> bool:
    """
    Check if the word exists among real dictionary words
    """
    if lang == "en":
        real_words = await RealWordEN.objects.all(string=string.lower())
        possible_duplicates = set()
        for w in real_words:
            possible_duplicates.add(w.string)
            if w.type == "noun" and w.number == "s":
                possible_duplicates.add(w.string + "s")
        if string.lower() in [w.lower() for w in possible_duplicates]:
            print(f"Word '{string}' already exists in English dictionnary.")
            return True
    if lang == "fr":
        real_words = await RealWordFR.objects.all(string=string)
        possible_duplicates = set()
        if string.lower() in [w.string.lower() for w in real_words]:
            print(f"Word '{string}' already exists in French dictionnary.")
            return True
    else:
        dictionary = []
        with open(f"{lang}/data/dictionary_{lang.upper()}.txt", "r") as dictionary_file:
            for word in dictionary_file:
                dictionary.append(word)
        if string in dictionary:
            print(f"Word '{string}' already exists in {lang} dictionnary.")
            return True
    return False