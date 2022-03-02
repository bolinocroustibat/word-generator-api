import os
import json
from pathlib import Path

import typer

from models import *


def classify(lang: str) -> None:

    # with open(f"{lang}/dictionary_{lang}.txt", "r") as dictionary_file:
    #     for word in dictionary_file:
    #         #TODO
    #         pass
    
    

if __name__ == "__main__":
    typer.run(classify)
