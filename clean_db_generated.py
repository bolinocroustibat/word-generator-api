from asyncio import run as aiorun

import typer

from models import (
    GeneratedWordEN,
    GeneratedWordFR,
    RealWordEN,
    RealWordFR,
    database,
)


def clean(lang: str) -> None:

    if lang not in ["en", "fr"]:
        typer.secho(f"Invalid language: {lang}", fg="red")
        raise typer.Abort()

    async def _main():

        if not database.is_connected:
            await database.connect()

        i = 0

        if lang == "en":
            for j, entry in enumerate(await GeneratedWordEN.objects.all()):
                existing = await RealWordEN.objects.all(string=entry.string)
                if existing:
                    i += 1
                    typer.secho(
                        f'"{entry.string}" exists as a real word. Deleting.', fg="cyan"
                    )
                    await entry.delete()
                else:
                    continue

        elif lang == "fr":
            for j, entry in enumerate(await GeneratedWordFR.objects.all()):
                existing = await RealWordFR.objects.all(string=entry.string)
                if existing:
                    i += 1
                    typer.secho(
                        f'"{entry.string}" exists as a real word. Deleting.', fg="cyan"
                    )
                    await entry.delete()
                else:
                    continue

        typer.secho(f'"{i}/{j}" generated words deleted from DB.', fg="green")

        if database.is_connected:
            await database.disconnect()

    aiorun(_main())


if __name__ == "__main__":
    typer.run(clean)
