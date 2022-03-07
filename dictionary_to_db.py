from asyncio import run as aiorun

import typer
from pymysql.err import IntegrityError

from en.classify import classify_en
from fr.classify import classify_fr
from models import RealWordEN, RealWordFR, database


def dictionary_to_db(lang: str) -> None:

    if lang not in ["en", "fr"]:
        raise typer.Abort(f"Invalid language: {lang}")

    async def _main():

        if not database.is_connected:
            await database.connect()

        with open(f"{lang}/data/dictionary_{lang.upper()}.txt", "r") as dictionary_file:
            i = 1
            for j, word in enumerate(dictionary_file):
                word = word.strip()
                if word:
                    if lang == "en":
                        word_classes = classify_en(word=word)
                        type: str = word_classes["type"]
                        number: str = word_classes["number"]
                        tense: str = word_classes["tense"]
                        try:
                            await RealWordEN.objects.get_or_create(
                                word=word, type=type, number=number, tense=tense
                            )
                        # except IntegrityError:
                        #     print(f"Word '{word}' was already in the DB.")
                        #     continue
                        except Exception as e:
                            typer.secho(f"{word}", fg=typer.colors.RED)
                            typer.secho(e, fg=typer.colors.RED)
                        else:
                            i += 1
                            typer.secho(f'"{word}" saved in DB.', fg=typer.colors.BLUE)
                    elif lang == "fr":
                        word_classes = classify_fr(word=word)
                        type: str = word_classes["type"]
                        gender: str = word_classes["gender"]
                        number: str = word_classes["number"]
                        tense: str = word_classes["tense"]
                        conjug: str = word_classes["conjug"]
                        try:
                            await RealWordFR.objects.get_or_create(
                                word=word,
                                type=type,
                                gender=gender,
                                number=number,
                                tense=tense,
                                conjug=conjug,
                            )
                        # except IntegrityError:
                        #     print(f"Word '{word}' was already in the DB.")
                        #     continue
                        except Exception as e:
                            typer.secho(f"{word}", fg=typer.colors.RED)
                            typer.secho(e, fg=typer.colors.RED)
                        else:
                            i += 1
                            typer.secho(f'"{word}" saved in DB.', fg=typer.colors.BLUE)

        typer.secho(f'"{i}/{j}" words saved in DB.', fg=typer.colors.GREEN)

        if database.is_connected:
            await database.disconnect()

    aiorun(_main())


if __name__ == "__main__":
    typer.run(dictionary_to_db)
