import asyncio

import typer
import tweepy

from config import (
    TWITTER_ACCESS_TOKEN,
    TWITTER_API_KEY,
    TWITTER_KEY_SECRET,
    TWITTER_TOKEN_SECRET,
)
from en.generate_definition import generate_definition_en
from models import database


async def generate_tweet():
    generated: dict = await generate_definition_en(percentage=0.4)
    string: str = generated["string"].capitalize()
    type: str = generated["type"]
    definition: str = generated["definition"]
    return f"{string} ({type}): {definition}"


async def send_tweet() -> None:

    if not database.is_connected:
        await database.connect()

    tweet: str = await generate_tweet()
    tries = 0
    while (len(tweet) > 275) and (tries < 6):
        # If tweet os too long, regenerate it.
        # Don't try more than 6 times for security reasons.
        tweet: str = await generate_tweet()
        tries += 1

    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_KEY_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_TOKEN_SECRET)

    api = tweepy.API(auth)
    api.update_status(tweet)
    typer.secho(f"Tweet posted:", fg="green", bold=True)
    typer.secho(tweet, fg="green")

    if database.is_connected:
        await database.disconnect()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    coroutine = send_tweet()
    generated: dict = loop.run_until_complete(coroutine)
