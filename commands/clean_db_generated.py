from asyncio import run as aiorun

import typer

from common.db import prepare_db
from models import GeneratedWord, Language, RealWord


def clean(lang: str) -> None:
    if lang not in ["en", "fr"]:
        typer.secho(f"Invalid language: {lang}", fg="red")
        raise typer.Abort()

    async def _main():
        i = 0

        await prepare_db()

        # Get language ID
        language = await Language.get(code=lang)

        # Get all generated words for this language
        generated_words = await GeneratedWord.filter(language=language)
        for j, entry in enumerate(generated_words):
            existing = await RealWord.filter(language=language, string=entry.string)
            if existing:
                i += 1
                typer.secho(f'"{entry.string}" exists as a real word. Deleting.', fg="cyan")
                await entry.delete()
            else:
                continue

        typer.secho(f'"{i}/{j}" generated words deleted from DB.', fg="green")

    aiorun(_main())


if __name__ == "__main__":
    typer.run(clean)
