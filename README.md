# Word Generator API in Python


## Main dependencies

Python API with a PostgreSQL database, using FastAPI framework.

- Python >=3.11
- [uv](https://docs.astral.sh/uv/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Tortoise ORM](https://tortoise-orm.readthedocs.io/)
- A PostgreSQL 15 database (not tested with other PostgreSQL versions)


## Endpoints

- `/docs`:
  Display the documentation of the API, with the availables endpoints, parameters, and provide a testing interface.
  Method: `GET`

- `/{lang}/generate`:
  Generate a new word that doesn't exist, and stores it in the DB.
  Available `lang`: `en`, `fr`, `it`, `es`
  Method: `GET`

- `/{lang}/get`:
  Get a random word that doesn't exist form the DB of generated words.
  Available `lang`: `en`, `fr`, `it`, `es`
  Method: `GET`

- `/{lang}/alter`:
  Alter a text with random non existing words.
  Available `lang`: `en`, `fr`
  Other parameters:
    - `text`
    - `percentage`
  Method: `GET`

- `/{lang}/definition`:
  Generate a random fake/altered dictionnary definition.
  Available `lang`: `en`, `fr`
  Method: `GET`


## Install

Create a virtual environnement and install the dependencies in it with [uv](https://docs.astral.sh/uv/) single command:
```bash
uv sync
```

### Setup the config file

In `config.py`:

- `ALLOW_ORIGINS`: `list`
- `DATABASE_URL`: `string`

    example: `DATABASE_URL = "mysql://root:root@localhost:8889/words"`

- `DICTIONNARY_EN_API_URL`: `string`
- `ALLOWED_TYPES_EN`: `list`
- `ALLOWED_TYPES_FR`: `dict`

    example: `ALLOWED_TYPES_FR = {"nom": "noun", "verbe": "verb", "adjectif": "adjective", "adverbe": "adverb"}`

- `USERNAME`: `string`
- `PASSWORD`: `string`
- `TWITTER`: `dict`
- `SENTRY_DSN`: `string`

### Install French tagging data with Spacy

For the French language, you need to download the Spacy NLP data:
```bash
python3 -m spacy download fr_core_news_sm
```
or, with uv:
```bash
uv run python -m spacy download fr_core_news_sm
```

If any issue with the `fr_core_news_sm` model installing, one can install it manually with:
```bash
wget https://github.com/explosion/spacy-models/releases/download/fr_core_news_sm-3.5.0/fr_core_news_sm-3.5.0-py3-none-any.whl -P ./assets
unzip assets/fr_core_news_sm-3.5.0-py3-none-any.whl -d ./.venv/lib/python3.12/site-packages && chmod -R 777 ./.venv/lib/python3.12/site-packages/fr_core_news_sm
```

If any issue with pip in the venv for Spacy:
```bash
python3 -m ensurepip --default-pip
```

If Spacy lefff doesn't work, try to install it manually with pip and not with uv in the venv:
```bash
pip install spacy-lefff
```
or, with uv:
```bash
uv run pip install spacy-lefff
```


## Run the API

Launch the web server with:
```bash
uv run uvicorn api:app --reload
```

Inside the venv:
```bash
uvicorn api:app --reload
```

## Lint and format the code

Before contributing to the repository, it is necessary to initialize the pre-commit hooks:
```bash
pre-commit install
```
Once this is done, code formatting and linting, as well as import sorting, will be automatically checked before each commit.

Lint and format with:
```bash
uv run ruff check --fix && rye format
```

## Commands

  - `build_proba_file.py` + language: Create the probability file for the Markov chain
  - `batch_generate.py` + language: Generate a batch of words (500 by default) and save them in DB
  - `classify_db_generated.py` + language: Update the generated words in DB with their tense, conjugation, genre, number, etc.
  - `classify_db_real.py` + language (from a dictionary TXT file): Update the real words in DB with their tense, conjugation, genre, number, etc.
  - `tweet.py` + language + optional: `--dry-run`

To run the commands, use for example:
```bash
python3 -m commands.build_proba_file en
```


## Usefuls resources

http://www.nurykabe.com/dump/text/lists/
