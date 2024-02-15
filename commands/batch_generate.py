from asyncio import run as aiorun

import typer

from common import generate_word_and_save, prepare_db


def batch_generate(lang: str, number: int = 500) -> None:
    if lang not in ["en", "fr"]:
        typer.secho(f"Invalid language: {lang}", fg="red")
        raise typer.Abort()

    async def _main():
        await prepare_db()

        i = 0
        for i in range(number):
            response = await generate_word_and_save(lang=lang, ip="localhost")
            if response:
                typer.secho(f"'{response['string']}' saved to the DB.", fg="cyan")
            else:
                typer.secho("Too many retries.", fg="red")
            i += 1

        typer.secho(f"{i} words generated and saved in the DB.", fg="green")

    aiorun(_main())


if __name__ == "__main__":
    typer.run(batch_generate)
