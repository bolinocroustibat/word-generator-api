from asyncio import run as aiorun

import typer

from en.classify import classify_en
from fr.classify import classify_fr
from models import GenereratedWordEN, GenereratedWordFR, database


def classify(lang: str) -> None:

    if lang not in ["en", "fr"]:
        raise typer.Abort(f"Invalid language: {lang}")

    async def _main():

        if not database.is_connected:
            await database.connect()

        i = 0

        if lang == "en":
            for j, entry in enumerate(await GenereratedWordEN.objects.all()):
                word_classes = classify_en(word=entry.string)
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
            for j, entry in enumerate(await GenereratedWordFR.objects.all()):
                word_classes = classify_fr(word=entry.string)
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

        if database.is_connected:
            await database.disconnect()

    aiorun(_main())


if __name__ == "__main__":
    typer.run(classify)
