from asyncio import run as aiorun
from typing import Optional

import tweepy
import typer

from common import prepare_db
from config import TWITTER
from en import generate_tweet_en
from fr import generate_tweet_fr


async def _send_tweet(lang: str, dry_run: bool = False) -> None:

    await prepare_db()

    if lang == "en":
        tweet: str = await generate_tweet_en()
    elif lang == "fr":
        tweet = await generate_tweet_fr()
    tries = 0
    while (len(tweet) > 275) and (tries < 6):
        typer.secho(f"Generated tweet is too long, trying again...", fg="cyan")
        # If tweet os too long, regenerate it.
        # Don't try more than 6 times for security reasons.
        if lang == "en":
            tweet: str = await generate_tweet_en()
        if lang == "fr":
            tweet: str = await generate_tweet_fr()
        tries += 1

    if dry_run:
        typer.secho(f"Tweet (not posted):", fg="green", bold=True)
        typer.secho(tweet, fg="green")
    else:
        try:
            auth = tweepy.OAuthHandler(
                TWITTER[lang]["api_key"], TWITTER[lang]["key_secret"]
            )
            auth.set_access_token(
                TWITTER[lang]["access_token"], TWITTER[lang]["token_secret"]
            )
            api = tweepy.API(auth)
            api.update_status(tweet)
        except Exception as e:
            typer.secho(f"Error:\n{e}", fg="red", bold=True)
            typer.secho(tweet, fg="red")
        else:
            typer.secho(f"Tweet posted:", fg="green", bold=True)
            typer.secho(tweet, fg="green")


def main(
    lang: str = typer.Argument(..., help="Language ('en' or 'fr')"),
    dry_run: Optional[bool] = typer.Option(False, help="Dry run"),
):
    aiorun(_send_tweet(lang, dry_run))


if __name__ == "__main__":
    typer.run(main)
