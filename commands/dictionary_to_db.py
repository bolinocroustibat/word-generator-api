from asyncio import run as aiorun

import typer

from common import prepare_db
from en.classify import classify_en
from fr.classify import classify_fr
from models import RealWordEN, RealWordFR


def dictionary_to_db(lang: str, classify=True) -> None:
    if lang not in ["en", "fr"]:
        raise typer.Abort(f"Invalid language: {lang}")

    async def _main():
        await prepare_db()

        with open(f"{lang}/data/adverbs_{lang.upper()}.txt", "r") as dictionary_file:
            i = 1
            for j, word in enumerate(dictionary_file):
                word = word.strip()
                if word:
                    if lang == "en":
                        existing = await RealWordEN.objects.all(string=word)
                        if not existing:
                            try:
                                if classify:
                                    word_classes: dict = classify_en(word=word)
                                    await RealWordEN.objects.create(
                                        string=word,
                                        type=word_classes["type"],
                                        number=word_classes["number"],
                                        tense=word_classes["tense"],
                                    )
                                else:
                                    await RealWordEN.objects.create(string=word)
                            except Exception as e:
                                typer.secho(f"{word}", fg="red")
                                typer.secho(e, fg="red")
                            else:
                                i += 1
                                typer.secho(f'"{word}" saved in DB.', fg="cyan")
                        else:
                            typer.secho(f'"{word}" was already in the DB.', fg="yellow")
                    elif lang == "fr":
                        existing = await RealWordFR.objects.all(string=word)
                        if not existing:
                            try:
                                if classify:
                                    word_classes: dict = await classify_fr(word=word)
                                    await RealWordFR.objects.create(
                                        string=word,
                                        type=word_classes["type"],
                                        gender=word_classes["gender"],
                                        number=word_classes["number"],
                                        tense=word_classes["tense"],
                                        proper=False,
                                    )
                                else:
                                    await RealWordFR.objects.create(string=word, proper=False)
                            except Exception as e:
                                typer.secho(f"{word}", fg="red")
                                typer.secho(e, fg="red")
                            else:
                                i += 1
                                typer.secho(f'"{word}" saved in DB.', fg="cyan")
                        else:
                            typer.secho(f'"{word}" was already in the DB.', fg="yellow")

        typer.secho(f'"{i}/{j}" words saved in DB.', fg="green")

    aiorun(_main())


if __name__ == "__main__":
    typer.run(dictionary_to_db)
