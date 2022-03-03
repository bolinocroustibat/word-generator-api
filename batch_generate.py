from asyncio import run as aiorun

import typer

from common.generate_word import generate_word_and_save
from models import database


def batch_generate(lang: str, number: int = 100) -> None:

    if lang not in ["en", "fr"]:
        raise typer.Abort(f"Invalid language: {lang}")

    async def _main():

        if not database.is_connected:
            await database.connect()

        i = 0
        for i in range(number):
            response = await generate_word_and_save(lang=lang, ip="localhost")
            typer.secho(f"'{response['string']}' saved to the DB.", fg="blue")
            i += 1

        if database.is_connected:
            await database.disconnect()

        typer.secho(f"{i} words generated and saved in the DB.", fg=typer.colors.GREEN)

    aiorun(_main())


if __name__ == "__main__":
    typer.run(batch_generate)
