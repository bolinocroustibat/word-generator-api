from asyncio import run as aiorun

import typer

from common import prepare_db
from models import GeneratedWordEN, GeneratedWordFR, RealWordEN, RealWordFR


def clean(lang: str) -> None:

    if lang not in ["en", "fr"]:
        typer.secho(f"Invalid language: {lang}", fg="red")
        raise typer.Abort()

    async def _main():

        i = 0

        await prepare_db()

        if lang == "en":
            for j, entry in enumerate(await GeneratedWordEN.all()):
                existing = await RealWordEN.filter(string=entry.string)
                if existing:
                    i += 1
                    typer.secho(
                        f'"{entry.string}" exists as a real word. Deleting.', fg="cyan"
                    )
                    await entry.delete()
                else:
                    continue

        elif lang == "fr":
            for j, entry in enumerate(await GeneratedWordFR.all()):
                existing = await RealWordFR.filter(string=entry.string)
                if existing:
                    i += 1
                    typer.secho(
                        f'"{entry.string}" exists as a real word. Deleting.', fg="cyan"
                    )
                    await entry.delete()
                else:
                    continue

        typer.secho(f'"{i}/{j}" generated words deleted from DB.', fg="green")

    aiorun(_main())


if __name__ == "__main__":
    typer.run(clean)
