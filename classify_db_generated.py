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

        if lang == "en":
            for j, entry in enumerate(await GenereratedWordEN.objects.all()):
                i = 1
                word_classes = classify_en(word=entry.string)
                try:
                    await entry.update(
                        type=word_classes["type"],
                        number=word_classes["number"],
                        tense=word_classes["tense"],
                    )
                except Exception as e:
                    typer.secho(f"{entry.string}", fg=typer.colors.RED)
                    typer.secho(e, fg=typer.colors.RED)
                else:
                    i += 1
                    typer.secho(f'"{entry.string}" saved in DB.', fg=typer.colors.BLUE)

        elif lang == "fr":
            for j, entry in enumerate(await GenereratedWordFR.objects.all()):
                i = 1
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
                    typer.secho(f"{entry.string}", fg=typer.colors.RED)
                    typer.secho(e, fg=typer.colors.RED)
                else:
                    i += 1
                    typer.secho(f'"{entry.string}" saved in DB.', fg=typer.colors.BLUE)

        typer.secho(f'"{i}/{j}" words saved in DB.', fg=typer.colors.GREEN)

        if database.is_connected:
            await database.disconnect()

    aiorun(_main())


if __name__ == "__main__":
    typer.run(classify)
