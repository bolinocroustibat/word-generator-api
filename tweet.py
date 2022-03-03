import asyncio

import tweepy

from config import (
    TWITTER_ACCESS_TOKEN,
    TWITTER_API_KEY,
    TWITTER_KEY_SECRET,
    TWITTER_TOKEN_SECRET,
)
from en.generate_definition import generate_definition_en
from models import database


async def send_tweet() -> None:

    if not database.is_connected:
        await database.connect()

    generated: dict = await generate_definition_en()
    string: str = generated["string"].capitalize()
    type: str = generated["type"]
    definition: str = generated["definition"]

    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_KEY_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_TOKEN_SECRET)

    api = tweepy.API(auth)
    api.update_status(f"{string} ({type}): {definition}")

    if database.is_connected:
        await database.disconnect()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    coroutine = send_tweet()
    generated: dict = loop.run_until_complete(coroutine)
