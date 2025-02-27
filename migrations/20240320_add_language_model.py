import asyncio

from tortoise import Tortoise

from config import DATABASE_URL


# Old models (for reference during migration)
class RealWordEN:
    class Meta:
        table = "real_words_EN"


class RealWordFR:
    class Meta:
        table = "real_words_FR"


class GeneratedWordEN:
    class Meta:
        table = "generated_words_EN"


class GeneratedWordFR:
    class Meta:
        table = "generated_words_FR"


class GeneratedDefinitionEN:
    class Meta:
        table = "generated_definitions_EN"


class GeneratedDefinitionFR:
    class Meta:
        table = "generated_definitions_FR"


async def init_tortoise():
    await Tortoise.init(db_url=DATABASE_URL, modules={"models": ["models"]})
    await Tortoise.generate_schemas()


async def migrate_data():
    # Connect to the database
    await init_tortoise()

    try:
        # Start transaction
        connection = Tortoise.get_connection("default")
        await connection.execute_query("BEGIN TRANSACTION")

        print("Creating new language entries...")
        # Create languages
        from models import Language

        english = await Language.create(code="en", name="English")
        french = await Language.create(code="fr", name="French")
        italian = await Language.create(code="it", name="Italian")
        spanish = await Language.create(code="es", name="Spanish")

        print("Migrating real words...")
        # Migrate RealWords
        # English
        await connection.execute_query(
            """
            INSERT INTO real_words (string, language_id, type, number, tense)
            SELECT string, $1, type, number, tense
            FROM "real_words_EN"
        """,
            [english.id],
        )

        # French
        await connection.execute_query(
            """
            INSERT INTO real_words (string, language_id, type, gender, number, tense, proper, complex)
            SELECT string, $1, type, gender, number, tense, proper, complex
            FROM "real_words_FR"
        """,
            [french.id],
        )

        print("Migrating generated words...")
        # Migrate GeneratedWords
        # English
        await connection.execute_query(
            """
            INSERT INTO generated_words (string, language_id, type, number, tense, date, ip)
            SELECT string, $1, type, number, tense, date, ip
            FROM "generated_words_EN"
        """,
            [english.id],
        )

        # French
        await connection.execute_query(
            """
            INSERT INTO generated_words (string, language_id, type, gender, number, tense, conjug, date, ip)
            SELECT string, $1, type, gender, number, tense, conjug, date, ip
            FROM "generated_words_FR"
        """,
            [french.id],
        )

        print("Migrating definitions...")
        # Migrate English definitions using CTE
        await connection.execute_query(
            """
            WITH word_mapping AS (
                SELECT gw_old.id as old_id, gw_new.id as new_id
                FROM "generated_words_EN" gw_old
                JOIN generated_words gw_new
                    ON gw_new.string = gw_old.string
                    AND gw_new.language_id = $1
            )
            INSERT INTO generated_definitions (generated_word_id, text, date, ip)
            SELECT m.new_id, d.text, d.date, d.ip
            FROM "generated_definitions_EN" d
            JOIN word_mapping m ON d.generated_word_id = m.old_id
        """,
            [english.id],
        )

        # Migrate French definitions using CTE
        await connection.execute_query(
            """
            WITH word_mapping AS (
                SELECT gw_old.id as old_id, gw_new.id as new_id
                FROM "generated_words_FR" gw_old
                JOIN generated_words gw_new
                    ON gw_new.string = gw_old.string
                    AND gw_new.language_id = $1
            )
            INSERT INTO generated_definitions (generated_word_id, text, date, ip)
            SELECT m.new_id, d.text, d.date, d.ip
            FROM "generated_definitions_FR" d
            JOIN word_mapping m ON d.generated_word_id = m.old_id
        """,
            [french.id],
        )

        print("Dropping old tables...")
        # Drop tables in correct order (definitions first, then words)
        await connection.execute_query('DROP TABLE IF EXISTS "generated_definitions_EN"')
        await connection.execute_query('DROP TABLE IF EXISTS "generated_definitions_FR"')
        await connection.execute_query('DROP TABLE IF EXISTS "generated_words_EN"')
        await connection.execute_query('DROP TABLE IF EXISTS "generated_words_FR"')
        await connection.execute_query('DROP TABLE IF EXISTS "real_words_EN"')
        await connection.execute_query('DROP TABLE IF EXISTS "real_words_FR"')

        # Commit transaction
        await connection.execute_query("COMMIT")

        print("Migration completed successfully!")

    except Exception as e:
        # Rollback in case of error
        await connection.execute_query("ROLLBACK")
        print(f"Error during migration: {e}")
        raise

    finally:
        # Close connection
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(migrate_data())
