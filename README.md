# Word Generator in Python


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

## Configure

In `config.py`:

- `ALLOW_ORIGINS`: list
- `MYSQL_URL`: str
- `DICTIONNARY_EN_API_URL`: str
- `DATA_DIR`: str
- `ALLOWED_TYPES`: list


## Run 

Activate the virtual environement:
```sh
poetry shell
```

Launch the web server:
```sh
uvicorn api:app --reload
```

## Commands

  - `build.py`
  - `classify_db_generated.py`
  - `classify_db_real.py` (from a dictionary TXT file)
