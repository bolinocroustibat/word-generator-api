import typer
import tweepy

from common.prepare_db import prepare_db
from config import TWITTER
from en.generate_definition import generate_definition_en
from fr.generate_definition import generate_definition_fr


async def generate_tweet(lang: str) -> str:
    await prepare_db()
    if lang == "en":
        generated: dict = await generate_definition_en(percentage=0.4)
    elif lang == "fr":
        generated: dict = await generate_definition_fr(percentage=0.6)
    string: str = generated["string"].capitalize()
    type: str = generated["type"]
    definition: str = generated["definition"]
    return f"{string} ({type}): {definition}"


async def send_tweet(lang: str) -> None:

    if lang not in ["en", "fr"]:
        raise typer.Abort(f"Invalid language: {lang}")

    tweet: str = await generate_tweet(lang)
    tries = 0
    while (len(tweet) > 275) and (tries < 6):
        # If tweet os too long, regenerate it.
        # Don't try more than 6 times for security reasons.
        tweet: str = await generate_tweet()
        tries += 1

    auth = tweepy.OAuthHandler(TWITTER[lang]["api_key"], TWITTER[lang]["key_secret"])
    auth.set_access_token(TWITTER[lang]["access_token"], TWITTER[lang]["token_secret"])

    api = tweepy.API(auth)
    api.update_status(tweet)
    typer.secho(f"Tweet posted:", fg="green", bold=True)
    typer.secho(tweet, fg="green")
