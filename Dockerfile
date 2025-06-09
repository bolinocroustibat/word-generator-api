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

# Port configuration:
# EXPOSE documents which port the application uses (purely informational)
EXPOSE 8000

# Start the application using gunicorn
CMD uv run gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker api:app --bind 0.0.0.0:8000
