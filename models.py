import databases
import ormar
import sqlalchemy

from config import MYSQL_URL

metadata = sqlalchemy.MetaData()
database = databases.Database(MYSQL_URL)


class RealWordEN(ormar.Model):
    id: int = ormar.Integer(primary_key=True)
    word: str = ormar.String(max_length=100)
    type: str = ormar.String(max_length=16)
    gender: str = ormar.String(max_length=1)
    number: str = ormar.String(max_length=1)
    tense: str = ormar.String(max_length=16)
    complex: bool = ormar.Boolean()

    class Meta:
        tablename = "real_words_EN"
        database = database
        metadata = metadata


class RealWordFR(ormar.Model):
    id: int = ormar.Integer(primary_key=True)
    word: str = ormar.String(max_length=100)
    type: str = ormar.String(max_length=16)
    number: str = ormar.String(max_length=1)
    tense: str = ormar.String(max_length=16)
    date = ormar.DateTime()
    ip: str = ormar.String(max_length=16)

    class Meta:
        tablename = "real_words_EN"
        database = database
        metadata = metadata


class GenereratedWordEN(ormar.Model):
    id: int = ormar.Integer(primary_key=True)
    word: str = ormar.String(max_length=100)
    type: str = ormar.String(max_length=16)
    number: str = ormar.String(max_length=1)
    tense: str = ormar.String(max_length=16)
    date = ormar.DateTime()
    ip: str = ormar.String(max_length=16)

    class Meta:
        tablename = "generated_words_EN"
        database = database
        metadata = metadata


class GenereratedWordFR(ormar.Model):
    id: int = ormar.Integer(primary_key=True)
    word: str = ormar.String(max_length=100)
    type: str = ormar.String(max_length=16)
    gender: str = ormar.String(max_length=1)
    number: str = ormar.String(max_length=1)
    tense: str = ormar.String(max_length=16)
    conjug: str = ormar.String(max_length=16)
    date = ormar.DateTime()
    ip: str = ormar.String(max_length=16)

    class Meta:
        tablename = "generated_words_FR"
        database = database
        metadata = metadata
