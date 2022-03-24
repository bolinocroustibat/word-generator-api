import ormar
from typing import Optional

from sqlmodel import Field, SQLModel
from config import MYSQL_URL

# metadata = sqlalchemy.MetaData()
# database = databases.Database(MYSQL_URL)


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None

class RealWordEN(SQLModel):
    id: int = Field(primary_key=True)
    string: str = Field(max_length=50)
    type: Optional[str] = Field(max_length=16, nullable=True)
    number: Optional[str] = Field(max_length=1, nullable=True)
    tense: Optional[str] = Field(max_length=16, nullable=True)

    class Meta:
        tablename = "real_words_EN"
        database = database
        metadata = metadata
        constraints = [ormar.UniqueColumns("string")]


class RealWordFR(SQLModel):
    id: int = ormar.Integer(primary_key=True)
    string: str = Field(max_length=100)
    type: str = Field(max_length=16, nullable=True)
    gender: str = Field(max_length=1, nullable=True)
    number: str = Field(max_length=1, nullable=True)
    tense: str = Field(max_length=16, nullable=True)
    proper: bool = ormar.Boolean()
    complex: bool = ormar.Boolean(nullable=True)

    class Meta:
        tablename = "real_words_FR"
        database = database
        metadata = metadata
        constraints = [ormar.UniqueColumns("string", "type")]


class GeneratedWordEN(SQLModel):
    id: int = ormar.Integer(primary_key=True)
    string: str = Field(max_length=100)
    type: str = Field(max_length=16, nullable=True)
    number: str = Field(max_length=1, nullable=True)
    tense: str = Field(max_length=16, nullable=True)
    date = ormar.DateTime()
    ip: str = Field(max_length=16)

    class Meta:
        tablename = "generated_words_EN"
        database = database
        metadata = metadata
        constraints = [ormar.UniqueColumns("string")]


class GeneratedWordFR(SQLModel):
    id: int = ormar.Integer(primary_key=True)
    string: str = Field(max_length=100)
    type: str = Field(max_length=16, nullable=True)
    gender: str = Field(max_length=1, nullable=True)
    number: str = Field(max_length=1, nullable=True)
    tense: str = Field(max_length=16, nullable=True)
    conjug: str = Field(max_length=16, nullable=True)
    date = ormar.DateTime()
    ip: str = Field(max_length=16)

    class Meta:
        tablename = "generated_words_FR"
        database = database
        metadata = metadata
        constraints = [ormar.UniqueColumns("string")]
