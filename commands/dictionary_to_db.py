from asyncio import run as aiorun

import typer

from common.db import prepare_db
from en.classify import classify_en
from fr.classify import classify_fr
from models import Language, RealWord


def dictionary_to_db(lang: str, classify=True) -> None:
    if lang not in ["en", "fr"]:
        raise typer.Abort(f"Invalid language: {lang}")

    async def _main():
        await prepare_db()

        # Get language ID
        language = await Language.get(code=lang)

        with open(f"{lang}/data/adverbs_{lang.upper()}.txt", "r") as dictionary_file:
            i = 1
            for j, word in enumerate(dictionary_file):
                word = word.strip()
                if word:
                    existing = await RealWord.filter(language=language, string=word)
                    if not existing:
                        try:
                            if classify:
                                if lang == "en":
                                    word_classes: dict = classify_en(word=word)
                                    await RealWord.create(
                                        string=word,
                                        language=language,
                                        type=word_classes["type"],
                                        number=word_classes["number"],
                                        tense=word_classes["tense"],
                                    )
                                elif lang == "fr":
                                    word_classes: dict = classify_fr(word=word)
                                    await RealWord.create(
                                        string=word,
                                        language=language,
                                        type=word_classes["type"],
                                        gender=word_classes["gender"],
                                        number=word_classes["number"],
                                        tense=word_classes["tense"],
                                        proper=False,
                                    )
                            else:
                                await RealWord.create(
                                    string=word,
                                    language=language,
                                    proper=False if lang == "fr" else None,
                                )
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
