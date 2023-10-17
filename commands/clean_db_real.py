from asyncio import run as aiorun

import typer
from asyncpg.exceptions import IntegrityConstraintViolationError

from common import prepare_db
from models import RealWordEN, RealWordFR


def clean(lang: str) -> None:

    if lang not in ["en", "fr"]:
        typer.secho(f"Invalid language: {lang}", fg="red")
        raise typer.Abort()

    async def _main():

        if lang == "en":
            real_word_class = RealWordEN
        elif lang == "fr":
            real_word_class = RealWordFR
        else:
            typer.secho(f"Invalid language: {lang}", fg="red")
            raise typer.Abort()

        await prepare_db()

        i = 0

        for j, entry in enumerate(await real_word_class.objects.all()):
            if ".ADV" in entry.string:
                i += 1
                typer.secho(
                    f'"{entry.string}" have .ADV in string, fixing...', fg="cyan"
                )
                replacement = entry.string.replace(".ADV", "")
                try:
                    await entry.update(
                        string=replacement,
                        type="adverb",
                    )
                except IntegrityConstraintViolationError:  # not sure
                    existing = await real_word_class.objects.all(string=replacement)
                    typer.secho(
                        f'Cannot replace there are already {len(existing)} "{entry.string}" in the DB!',
                        fg="yellow",
                    )
                    for w in existing:
                        if w != entry:
                            # typer.secho(w.complex)
                            # typer.secho(entry.complex)
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

        typer.secho(
            f'"{i}/{j}" real words had .ADV in string and were fixed.', fg="green"
        )

    aiorun(_main())


if __name__ == "__main__":
    typer.run(clean)
