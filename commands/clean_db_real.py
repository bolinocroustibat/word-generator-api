from asyncio import run as aiorun

import typer
from asyncpg.exceptions import IntegrityConstraintViolationError

from common import prepare_db
from models import Language, RealWord


def clean(lang: str) -> None:
    if lang not in ["en", "fr"]:
        typer.secho(f"Invalid language: {lang}", fg="red")
        raise typer.Abort()

    async def _main():
        await prepare_db()

        # Get language ID
        language = await Language.get(code=lang)

        i = 0

        # Get all real words for this language
        real_words = await RealWord.filter(language=language)
        for j, entry in enumerate(real_words):
            if ".ADV" in entry.string:
                i += 1
                typer.secho(f'"{entry.string}" have .ADV in string, fixing...', fg="cyan")
                replacement = entry.string.replace(".ADV", "")
                try:
                    await entry.update(
                        string=replacement,
                        type="adverb",
                    )
                except IntegrityConstraintViolationError:  # not sure
                    existing = await RealWord.filter(language=language, string=replacement)
                    typer.secho(
                        f'Cannot replace there are already {len(existing)} "{entry.string}" in the DB!',
                        fg="yellow",
                    )
                    for w in existing:
                        if w != entry:
                            if w.complex is True and entry.complex is False:
                                await w.delete()
                                typer.secho("duplicate complex deleted.", fg="red")
                            if entry.complex is True and w.complex is False:
                                await w.delete()
                                typer.secho("duplicate complex deleted.", fg="red")
                    await entry.update(
                        string=replacement,
                        type="adverb",
                    )
                typer.secho("Done.")
            else:
                continue

        typer.secho(f'"{i}/{j}" real words had .ADV in string and were fixed.', fg="green")

    aiorun(_main())


if __name__ == "__main__":
    typer.run(clean)
