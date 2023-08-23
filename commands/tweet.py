from asyncio import run as aiorun
from typing import Optional

import requests
import tweepy
import typer

from common import prepare_db
from config import SENTRY_DSN, SENTRY_CRON_MONITOR_ID, TWITTER
from en import generate_tweet_en
from fr import generate_tweet_fr


async def _send_tweet(lang: str, dry_run: bool = False) -> None:
    SENTRY_HEADERS = {
        "Authorization": "DSN " + SENTRY_DSN,
        "Content-Type": "application/json",
    }
    SENTRY_ORG_SLUG = "adrien-carpentier"  # Write your organization slug here

    await prepare_db()

    tweet: Optional[str] = None
    if lang == "en":
        tweet = await generate_tweet_en()
    elif lang == "fr":
        tweet = await generate_tweet_fr()

    sentry_monitor_id = SENTRY_CRON_MONITOR_ID[lang]
    # SENTRY: Create the check-in
    json_data = {"status": "in_progress"}
    response = requests.post(
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
                tweet: str = await generate_tweet_en()
            if lang == "fr":
                tweet: str = await generate_tweet_fr()
            tries += 1

        if dry_run:
            typer.secho("Tweet (not posted):", fg="green", bold=True)
            typer.secho(tweet, fg="green")
        else:
            try:
                client = tweepy.Client(
                    consumer_key=TWITTER[lang]["api_key"],
                    consumer_secret=TWITTER[lang]["key_secret"],
                    access_token=TWITTER[lang]["access_token"],
                    access_token_secret=TWITTER[lang]["token_secret"],
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
    response = requests.put(
        f"https://sentry.io/api/0/organizations/{SENTRY_ORG_SLUG}/monitors/{sentry_monitor_id}/checkins/{checkin_id}/",
        headers=SENTRY_HEADERS,
        json=json_data,
    )


def main(
    lang: str = typer.Argument(..., help="Language ('en' or 'fr')"),
    dry_run: Optional[bool] = typer.Option(False, help="Dry run"),
):
    aiorun(_send_tweet(lang, dry_run))


if __name__ == "__main__":
    typer.run(main)
