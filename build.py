import json
import os
from pathlib import Path

import typer


def build_proba_table(lang: str) -> None:
    with open(f"{lang}/data/alphabet_{lang.upper()}.json", "r") as alphabet_file:
        alphabet = json.load(alphabet_file)

    # build output structure
    # TODO

    with open(f"{lang}/data/dictionary_{lang.upper()}.txt", "r") as dictionary_file:
        for word in dictionary_file:
            # TODO
            pass


if __name__ == "__main__":
    typer.run(build_proba_table)
