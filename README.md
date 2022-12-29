# Word Generator API in Python


## Main dependencies

Python API with a MySQL database, using FastAPI framework.

- Python 3.9 (also tested successfully with 3.7)
- [Poetry](https://python-poetry.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Tortoise ORM](https://tortoise-orm.readthedocs.io/)
- MySQL/MariaDB database

## Install

Create a virtual environnement and install the dependencies in it with Poetry single command:
```sh
poetry install
```

### Setup the config file

In `config.py`:

- `ALLOW_ORIGINS`: list
- `DATABASE_URL`: string
    example: `DATABASE_URL = "mysql://root:root@localhost:8889/words"`
- `DICTIONNARY_EN_API_URL`: string
- `ALLOWED_TYPES_EN`: list
- `ALLOWED_TYPES_FR`: dict
    example: `ALLOWED_TYPES_FR = {"nom": "noun", "verbe": "verb", "adjectif": "adjective", "adverbe": "adverb"}`
- `USERNAME`: string
- `PASSWORD`: string
- `TWITTER`: dict
- `SENTRY_DSN`: string


### Install French tagging data with Spacy


For the French language, you need to download the Spacy NLP data:
```sh
python -m spacy download fr_core_news_sm
```
If Spacy lefff doesn't work, try to install it manually with pip and not with poetry in the venv:
```sh
pip install spacy-lefff
```

## Run the API

Activate the virtual environement:
```sh
poetry shell
```

Launch the web server:
```sh
uvicorn api:app --reload
```


## Commands

  - `batch_generate.py` + language
  - `build.py`
  - `classify_db_generated.py` + language
  - `classify_db_real.py` + language (from a dictionary TXT file)
  - `tweet.py` + language + optional: `--dry-run`


# Usefuls resources

http://www.nurykabe.com/dump/text/lists/
