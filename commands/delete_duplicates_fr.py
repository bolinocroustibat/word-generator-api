from asyncio import run as aiorun

import typer
from tqdm import tqdm

from common.db import prepare_db
from models import Language, RealWord


def delete_duplicates_fr() -> None:
    async def _main():
        await prepare_db()

        # Get French language ID
        french = await Language.get(code="fr")

        # Get all real words for French
        entries = await RealWord.filter(language=french)
        for e in tqdm(entries):
            similar_entries = await RealWord.filter(language=french, string=e.string, type=e.type)
            if len(similar_entries) > 1:
                for s in similar_entries:
                    if s.id != e.id:
                        try:
                            if s.gender != e.gender:
                                s.update(gender=None)
                                e.update(gender=None)
                        except Exception as e:
                            pass
                        if s.complex is True and e.complex is False:
                            print(f"1. Deleting {s.string} (id {s.id})\n")
                            await s.delete()
                        elif s.complex is False and e.complex is True:
                            print(f"2. Deleting {e.string} (id {e.id})\n")
                            await e.delete()
                        else:
                            if s.id > e.id:
                                print(f"3. Deleting {s.string} (id {s.id})\n")
                                await s.delete()
                            else:
                                print(f"4. Deleting {e.string} (id {e.id})\n")
                                await e.delete()

    aiorun(_main())


if __name__ == "__main__":
    typer.run(delete_duplicates_fr)
