import databases
import ormar
import sqlalchemy

from config import MYSQL_URL

metadata = sqlalchemy.MetaData()
database = databases.Database(MYSQL_URL)


class RealWordEN(ormar.Model):
    id: int = ormar.Integer(primary_key=True)
    string: str = ormar.String(max_length=50)
    type: str = ormar.String(max_length=16, nullable=True)
    number: str = ormar.String(max_length=1, nullable=True)
    tense: str = ormar.String(max_length=16, nullable=True)

    class Meta:
        tablename = "real_words_EN"
        database = database
        metadata = metadata


class RealWordFR(ormar.Model):
    id: int = ormar.Integer(primary_key=True)
    string: str = ormar.String(max_length=100)
    type: str = ormar.String(max_length=16, nullable=True)
    gender: str = ormar.String(max_length=1, nullable=True)
    number: str = ormar.String(max_length=1, nullable=True)
    tense: str = ormar.String(max_length=16, nullable=True)
    proper: bool = ormar.Boolean()
    complex: bool = ormar.Boolean(nullable=True)

    class Meta:
        tablename = "real_words_FR"
        database = database
        metadata = metadata


class GenereratedWordEN(ormar.Model):
    id: int = ormar.Integer(primary_key=True)
    string: str = ormar.String(max_length=100)
    type: str = ormar.String(max_length=16, nullable=True)
    number: str = ormar.String(max_length=1, nullable=True)
    tense: str = ormar.String(max_length=16, nullable=True)
    date = ormar.DateTime()
    ip: str = ormar.String(max_length=16)

    class Meta:
        tablename = "generated_words_EN"
        database = database
        metadata = metadata
        constraints = [ormar.UniqueColumns("string")]


class GenereratedWordFR(ormar.Model):
    id: int = ormar.Integer(primary_key=True)
    string: str = ormar.String(max_length=100)
    type: str = ormar.String(max_length=16, nullable=True)
    gender: str = ormar.String(max_length=1, nullable=True)
    number: str = ormar.String(max_length=1, nullable=True)
    tense: str = ormar.String(max_length=16, nullable=True)
    conjug: str = ormar.String(max_length=16, nullable=True)
    date = ormar.DateTime()
    ip: str = ormar.String(max_length=16)

    class Meta:
        tablename = "generated_words_FR"
        database = database
        metadata = metadata
        constraints = [ormar.UniqueColumns("string")]
