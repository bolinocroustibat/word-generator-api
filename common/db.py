import os

from dotenv import load_dotenv
from tortoise import Tortoise

load_dotenv()


def get_database_url(host: str | None = None) -> str:
    """
    Build database URL from individual components.
    In Docker, the host should be the service name 'db'.
    In local development, it defaults to 'localhost'.
    """
    # In Docker, the host should be the service name 'db'
    if host is None:
        host = "db" if os.getenv("ENVIRONMENT") != "local" else "localhost"

    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    db = os.getenv("POSTGRES_DB")
    port = os.getenv("POSTGRES_PORT", "5432")

    return f"postgres://{user}:{password}@{host}:{port}/{db}"


async def prepare_db():
    """Initialize database connection with Tortoise ORM."""
    await Tortoise.init(db_url=get_database_url(), modules={"models": ["models"]})
