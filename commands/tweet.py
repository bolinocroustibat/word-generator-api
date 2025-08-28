import os
from asyncio import run as aiorun

import httpx
import tweepy
import typer
from dotenv import load_dotenv

from common.db import prepare_db
from en import generate_tweet_en
from fr import generate_tweet_fr

load_dotenv()


async def _send_tweet(lang: str, dry_run: bool = False) -> None:
    SENTRY_DSN = os.getenv("SENTRY_DSN")
    SENTRY_HEADERS = {
        "Authorization": "DSN " + SENTRY_DSN,
        "Content-Type": "application/json",
    }
    SENTRY_ORG_SLUG = "adrien-carpentier"  # Write your organization slug here

    await prepare_db()

    tweet: str | None = None
    if lang == "en":
        tweet = await generate_tweet_en()
    elif lang == "fr":
        tweet = await generate_tweet_fr()

    sentry_monitor_id = os.getenv(f"SENTRY_CRON_MONITOR_ID_{lang.upper()}")
    # SENTRY: Create the check-in
    json_data = {"status": "in_progress"}
    with httpx.Client() as client:
        response = client.post(
            f"https://sentry.io/api/0/organizations/{SENTRY_ORG_SLUG}/monitors/{sentry_monitor_id}/checkins/",
            headers=SENTRY_HEADERS,
            json=json_data,
        )
        checkin_id = response.json()["id"]

    if tweet:
        tries = 0
        while (len(tweet) > 275) and (tries < 6):
            typer.secho("Generated tweet is too long, trying again...", fg="cyan")
            # If tweet os too long, regenerate it.
            # Don't try more than 6 times for security reasons.
            if lang == "en":
                tweet = await generate_tweet_en()
            if lang == "fr":
                tweet = await generate_tweet_fr()
            tries += 1

        if dry_run:
            typer.secho("Tweet (not posted):", fg="green", bold=True)
            typer.secho(tweet, fg="green")
        else:
            try:
                client = tweepy.Client(
                    consumer_key=os.getenv(f"TWITTER_{lang.upper()}_API_KEY"),
                    consumer_secret=os.getenv(f"TWITTER_{lang.upper()}_KEY_SECRET"),
                    access_token=os.getenv(f"TWITTER_{lang.upper()}_ACCESS_TOKEN"),
                    access_token_secret=os.getenv(f"TWITTER_{lang.upper()}_TOKEN_SECRET"),
                )
                response = client.create_tweet(text=tweet)
            except Exception as e:
                typer.secho(f"Error:\n{e}", fg="red", bold=True)
                typer.secho(tweet, fg="red")
            else:
                typer.secho("Tweet posted:", fg="green", bold=True)
                typer.secho(tweet, fg="green")

    # SENTRY: Update the check-in status (required) and duration (optional)
    json_data = {"status": "ok"}
    with httpx.Client() as client:
        response = client.put(
            f"https://sentry.io/api/0/organizations/{SENTRY_ORG_SLUG}/monitors/{sentry_monitor_id}/checkins/{checkin_id}/",
            headers=SENTRY_HEADERS,
            json=json_data,
        )


def main(
    lang: str = typer.Argument(..., help="Language ('en' or 'fr')"),
    dry_run: bool = typer.Option(False, help="Dry run"),
):
    aiorun(_send_tweet(lang, dry_run))


if __name__ == "__main__":
    typer.run(main)
