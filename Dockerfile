# Use Python 3.12 as base image
FROM python:3.12-slim
# Copy latest uv binary from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Python environment variables:
# PYTHONDONTWRITEBYTECODE=1: Prevents Python from writing .pyc files (speeds up development and reduces container size)
# PYTHONUNBUFFERED=1: Prevents Python from buffering stdout/stderr (ensures log messages are output immediately)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy the project into the image
ADD . /app

# Set work directory and install dependencies in a new environment
WORKDIR /app
# Sync the project, asserting the lockfile is up to date
RUN uv sync --locked

# Install required packages and download language models
RUN apt-get update && \
    # Install temporary packages (wget and unzip) needed for downloads
    apt-get install -y --no-install-recommends wget unzip && \
    # Download and install French spaCy model
    wget https://github.com/explosion/spacy-models/releases/download/fr_core_news_sm-3.5.0/fr_core_news_sm-3.5.0-py3-none-any.whl -P /tmp && \
    unzip /tmp/fr_core_news_sm-3.5.0-py3-none-any.whl -d ./.venv/lib/python3.12/site-packages && \
    # Download NLTK data using uv
    uv run python -m nltk.downloader averaged_perceptron_tagger_eng punkt_tab && \
    # Download and set up spacy-lefff model files
    mkdir -p ./.venv/lib/python3.12/site-packages/spacy_lefff/data/tagger/models/fr && \
    wget https://github.com/sammous/spacy-lefff-model/releases/download/v0.1.1/model.tar.gz -P /tmp && \
    tar -xzf /tmp/model.tar.gz -C /tmp && \
    cp -r /tmp/models/fr/* ./.venv/lib/python3.12/site-packages/spacy_lefff/data/tagger/models/fr/ && \
    chmod -R 777 ./.venv/lib/python3.12/site-packages/spacy_lefff/data && \
    # Cleanup temporary files and packages
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* && \
    apt-get purge -y wget unzip && \
    apt-get autoremove -y

# Port configuration:
# EXPOSE documents which port the application uses (purely informational)
EXPOSE 8000

# Start the application using gunicorn
CMD uv run gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker api:app --bind 0.0.0.0:8000
