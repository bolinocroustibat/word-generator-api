from tortoise import Tortoise

from config import DATABASE_URL


async def prepare_db():
    await Tortoise.init(db_url=DATABASE_URL, modules={"models": ["models"]})
