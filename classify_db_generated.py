import asyncio
import json
from operator import ge
import os
from asyncio import run as aiorun
from pathlib import Path

import typer

from en.classify import classify_en
from fr.classify import classify_fr
from models import GenereratedWordEN, GenereratedWordFR, database


def classify(lang: str) -> None:



    async def _main():

        if not database.is_connected:
            await database.connect()

        if lang == "en":
            for j, entry in enumerate(await GenereratedWordEN.objects.all()):
                i = 1
                word = entry.string
                word_classes = classify_en(word=word)
                try:
                    await entry.update(type=word_classes["type"], number=word_classes["number"], tense=word_classes["tense"])
                except Exception as e:
                    typer.secho(f"{word}", fg=typer.colors.RED)
                    typer.secho(e, fg=typer.colors.RED)
                else:
                    i += 1
                    typer.secho(f'"{word}" saved in DB.', fg=typer.colors.BLUE)

            typer.secho(f'"{i}/{j}" words saved in DB.', fg=typer.colors.GREEN)
        
        else:
            raise typer.Abort(f"Invalid language: {lang}")

        if database.is_connected:
            await database.disconnect()

    aiorun(_main())


if __name__ == "__main__":
    typer.run(classify)
