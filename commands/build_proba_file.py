import json
from asyncio import run as aiorun
from pathlib import Path

import typer


def build_1char_probabilities(
    alphabet: list[str], dictionary_filepath: Path, json_filepath: Path
) -> dict[str, dict[str, int]]:
    # Initialize the nested dictionary structure
    temp: dict[str, int] = {char: 0 for char in alphabet}
    temp["last_letter"] = 0
    probabilities: dict[str, dict[str, int]] = {"first_letter": temp}
    for char in alphabet:
        probabilities[char] = temp

    # Populate the dictionary with probabilities
    with open(dictionary_filepath, "r", encoding="utf-8") as dictionary:
        for line in dictionary:
            word: str = line.strip()
            first_letter: str = word[0].lower()
            probabilities["first_letter"][first_letter] += 1
            i = 0
            while i < len(word) and word[i].lower() in alphabet:
                current_char = word[i].lower()
                next_char = word[i + 1].lower() if i + 1 < len(word) else None
                if next_char is None or next_char not in alphabet:
                    probabilities[current_char]["last_letter"] += 1
                    break
                else:
                    probabilities[current_char][next_char] += 1
                i += 1

    return probabilities


def build_2char_probabilities(
    alphabet: list[str], dictionary_filepath: Path, json_filepath: Path
) -> dict:
    # Initialize the nested dictionary structure
    temp: dict = {}
    for letter1 in alphabet:
        for letter2 in alphabet:
            temp[letter1 + letter2] = 0

    alphabet_dict: dict = {char: 0 for char in alphabet}

    temp2: dict = alphabet_dict | temp
    temp3: dict = alphabet_dict | {"last_letter": 0}

    probabilities: dict = {"first_letter": alphabet_dict} | {
        chars: temp3.copy() for chars in temp2
    }

    # Populate the dictionary with probabilities
    with open(dictionary_filepath, "r", encoding="utf-8") as dictionary:
        for line in dictionary:
            word: str = line.strip()
            first_letter: str = word[0].lower()
            if first_letter in alphabet:
                probabilities["first_letter"][first_letter] += 1
                second_letter = word[1].lower() if len(word) > 1 else None
                if second_letter is not None and second_letter in alphabet:
                    probabilities[first_letter][second_letter] += 1
                    third_letter = word[2].lower() if len(word) > 2 else None
                    if third_letter is None:
                        probabilities[first_letter + second_letter]["last_letter"] += 1
                    else:
                        i = 0
                        while i < len(word):
                            char1 = word[i].lower()
                            char2 = word[i + 1].lower() if i + 1 < len(word) else None
                            char3 = word[i + 2].lower() if i + 2 < len(word) else None
                            if char2 in alphabet and char3 in alphabet:
                                probabilities[char1 + char2][char3] += 1
                            elif char2 in alphabet and char3 not in alphabet:
                                probabilities[char1 + char2]["last_letter"] += 1
                                break
                            elif char2 not in alphabet:
                                probabilities[char1]["last_letter"] += 1
                                break
                            i += 1

    return probabilities


def build_chars_probability_file(lang: str, chars_nb: int = 2) -> None:
    if lang not in ["en", "es", "fr", "it"]:
        typer.secho(f"Invalid language: {lang}", fg="red")
        raise typer.Abort()

    if chars_nb not in [1, 2]:
        typer.secho(f"Invalid nb of chars: {chars_nb}", fg="red")
        raise typer.Abort()

    async def _main():
        current_path = Path(__file__).parent.absolute()

        with open(
            current_path / f"../{lang}/data/alphabet_{lang.upper()}.json"
        ) as infile:
            alphabet: list[str] = json.load(infile)

        dictionary_filepath: Path = (
            current_path / f"../{lang}/data/dictionary_{lang.upper()}.txt"
        )
        json_filepath: Path = (
            current_path
            / f"../{lang}/data/proba_table_{chars_nb}char_{lang.upper()}.json"
        )

        if chars_nb == 1:
            probabilities: dict = build_1char_probabilities(
                alphabet, dictionary_filepath, json_filepath
            )
        elif chars_nb == 2:
            probabilities: dict = build_2char_probabilities(
                alphabet, dictionary_filepath, json_filepath
            )

        with open(json_filepath, "w", encoding="utf-8") as outfile:
            json.dump(probabilities, outfile, ensure_ascii=False)

        typer.secho(f"File generated as {dictionary_filepath}.", fg="green")

    aiorun(_main())


if __name__ == "__main__":
    typer.run(build_chars_probability_file)
