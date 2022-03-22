# Word Generator API in Python


## Main dependencies

Python API with a MySQL database, using FastAPI framework.

- Python 3.9 (also tested successfully with 3.7)
- [Poetry](https://python-poetry.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Ormar](https://collerek.github.io/ormar/) ORM
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
    - local: DATABASE_URL = "mysql://root:root@localhost:8889/words"
    - production: DATABASE_URL = "mysql://localmysqluser:localpasswd@localhost/words"
- `DICTIONNARY_EN_API_URL`: string
- `ALLOWED_TYPES_EN`: list
- `ALLOWED_TYPES_FR`: dict
    example: ALLOWED_TYPES_FR = {"nom": "noun", "verbe": "verb", "adjectif": "adjective", "adverbe": "adverb"}
- `TWITTER_API_KEY`: string
- `TWITTER_API_SECRET`: string
- `TWITTER_ACCESS_TOKEN`: string
- `TWITTER_TOKEN_SECRET`: string


### Configure French tagging with Treetagger

For the French language, you need to download the Treetagger and configure it. We'll follow those intructions:
https://hugonlp.wordpress.com/2015/10/07/how-to-do-pos-tagging-and-lemmatization-in-languages-other-than-english/

Export env variable (it's one of the two but I don't know which one):
```bash
export TREETAGGER_HOME='/Users/bolino/code/perso/word-generator-api/fr/treetagger'
export TREETAGGER='/Users/bolino/code/perso/word-generator-api/fr/treetagger'
```

Install Treetagger:
```bash
cd fr/treetagger
./install-tagger-fr-linux.py
```

Install Treetagger-python:
```bash
cd fr/treetagger-python
python setup.py install
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
  - `classify_db_real.py` +language (from a dictionary TXT file)
  - `tweet.py`


# Usefuls resources

http://www.nurykabe.com/dump/text/lists/
