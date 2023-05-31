# Word Generator API in Python


## Main dependencies

Python API with a MySQL/MariaDB database, using Litestar framework.

- Python 3.9 (also tested successfully with 3.7)
- [PDM](https://pdm.fming.dev/)
- [Litestar](https://github.com/litestar-org/litestar)
- [Tortoise ORM](https://tortoise-orm.readthedocs.io/)
- MySQL/MariaDB database

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

Create a virtual environnement and install the dependencies in it with [PDM](https://pdm.fming.dev/) single command:
```bash
pdm install
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
or, with PDM:
```bash
pdm run python -m spacy download fr_core_news_sm
```

If any issue with the `fr_core_news_sm` model installing, one can install it manually with:
```bash
wget https://github.com/explosion/spacy-models/releases/download/fr_core_news_sm-3.5.0/fr_core_news_sm-3.5.0-py3-none-any.whl -P ./assets
unzip assets/fr_core_news_sm-3.5.0-py3-none-any.whl -d ./.venv/lib/python3.9/site-packages
```

If any issue with pip in the venv for Spacy:
```bash
python3 -m ensurepip --default-pip
```

If Spacy lefff doesn't work, try to install it manually with pip and not with PDM in the venv:
```bash
pip install spacy-lefff
```
or, with PDM:
```bash
pdm run pip install spacy-lefff
```

## Run the API

Launch the web server with:
```bash
uvicorn app:app --reload
```
Inside the venv:
```bash
pdm run uvicorn app:app --reload
```

## Commands

  - `batch_generate.py` + language
  - `build.py`
  - `classify_db_generated.py` + language
  - `classify_db_real.py` + language (from a dictionary TXT file)
  - `tweet.py` + language + optional: `--dry-run`

To run the commands, use for example:
```bash
python3 -m commands.batch_generate.py en
```

# Usefuls resources

http://www.nurykabe.com/dump/text/lists/
