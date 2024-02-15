from asyncio import run as aiorun

import typer

from common import prepare_db
from en.classify import classify_en
from fr.classify import classify_fr
from models import GeneratedWordEN, GeneratedWordFR


def classify(lang: str) -> None:
    if lang not in ["en", "fr"]:
        raise typer.Abort(f"Invalid language: {lang}")

    async def _main():
        await prepare_db()

        i = 0

        if lang == "en":
            for j, entry in enumerate(await GeneratedWordEN.all()):
                word_classes: dict = classify_en(word=entry.string)
                try:
                    await entry.update(
                        type=word_classes["type"],
                        number=word_classes["number"],
                        tense=word_classes["tense"],
                    )
                except Exception as e:
                    typer.secho(f"{entry.string}", fg="red")
                    typer.secho(e, fg="red")
                else:
                    i += 1
                    typer.secho(f'"{entry.string}" updated.', fg="cyan")

        elif lang == "fr":
            for j, entry in enumerate(await GeneratedWordFR.all()):
                word_classes: dict = classify_fr(word=entry.string)
                try:
                    await entry.update(
                        type=word_classes["type"],
                        number=word_classes["number"],
                        gender=word_classes["gender"],
                        tense=word_classes["tense"],
                        conjug=word_classes["conjug"],
                    )
                except Exception as e:
                    typer.secho(f"{entry.string}", fg="red")
                    typer.secho(e, fg="red")
                else:
                    i += 1
                    typer.secho(f'"{entry.string}" updated.', fg="cyan")

        typer.secho(f'"{i}/{j}" generated words updated in DB.', fg="green")

    aiorun(_main())


if __name__ == "__main__":
    typer.run(classify)
