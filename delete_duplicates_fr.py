from asyncio import run as aiorun

import typer
from tqdm import tqdm

from models import RealWordFR, database


def delete_duplicates_fr() -> None:
    async def _main():

        if not database.is_connected:
            await database.connect()

        entries = await RealWordFR.objects.all()
        for e in tqdm(entries):
            similar_entries = await RealWordFR.objects.all(string=e.string, type=e.type)
            if len(similar_entries) > 1:
                for s in similar_entries:
                    if s.id != e.id:
                        try:
                            if s.gender != e.gender:
                                s.update(gender=None)
                                e.update(gender=None)
                        except:
                            pass
                        if s.complex == True and e.complex == False:
                            print(f"1. Deleting {s.string} (id {s.id})\n")
                            await s.delete()
                        elif s.complex == False and e.complex == True:
                            print(f"2. Deleting {e.string} (id {e.id})\n")
                            await e.delete()
                        else:
                            if s.id > e.id:
                                print(f"3. Deleting {s.string} (id {s.id})\n")
                                await s.delete()
                            else:
                                print(f"4. Deleting {e.string} (id {e.id})\n")
                                await e.delete()

        if database.is_connected:
            await database.disconnect()

    aiorun(_main())


if __name__ == "__main__":
    typer.run(delete_duplicates_fr)
