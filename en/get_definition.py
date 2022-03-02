import json
import requests

from config import DICTIONNARY_API_URL


def get_definition_en(word: str) -> str:
    """
    Returns the definition of the word.
    """
    response = requests.get(f"{DICTIONNARY_API_URL}{word}")
    definitions: list = response.json()[0]["meanings"]
    print(definitions)
    return definitions
