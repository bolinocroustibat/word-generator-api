install:
	@python -m pip install --upgrade pip
	@poetry install

format:
	@poetry run isort .
	@poetry run black .

# requirements.txt is only used for GitHub vulnerability alert.
# GitHub does not support poetry yet, so this file is needed.
# <https://docs.github.com/en/free-pro-team@latest/github/visualizing-repository-data-with-graphs/about-the-dependency-graph#supported-package-ecosystems>
requirements:
	@poetry export --without-hashes -f requirements.txt -o requirements.txt

check-types:
	@poetry run mypy

run:
	@poetry run uvicorn app:app --reload
