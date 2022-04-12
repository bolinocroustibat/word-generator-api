from asyncio import run as aiorun
from pymysql.err import IntegrityError

import typer

from common.prepare_db import prepare_db
from models import RealWordFR, database


def clean(lang: str) -> None:

    if lang not in ["en", "fr"]:
        typer.secho(f"Invalid language: {lang}", fg="red")
        raise typer.Abort()

    async def _main():

        await prepare_db()

        i = 0

        if lang == "fr":
            for j, entry in enumerate(await RealWordFR.objects.all()):
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
                    except IntegrityError:
                        existing = await RealWordFR.objects.all(string=replacement)
                        typer.secho(
                            f'Cannot replace there are already {len(existing)} "{entry.string}" in the DB!',
                            fg="yellow",
                        )
                        for w in existing:
                            if w != entry:
                                print(w.complex)
                                print(entry.complex)
                                if w.complex == True and entry.complex == False:
                                    await w.delete()
                                    typer.secho("duplicate complex deleted.", fg="red")
                                if entry.complex == True and w.complex == False:
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
