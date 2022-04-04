from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, create_engine

from config import MYSQL_URL


class RealWordEN(SQLModel, table=True):
    id: int = Field(primary_key=True)
    string: str
    type: Optional[str]
    number: Optional[str]
    tense: Optional[str]

    __tablename__ = "real_words_EN"


class RealWordFR(SQLModel, table=True):
    id: int = Field(primary_key=True)
    string: str
    type: Optional[str]
    gender: Optional[str]
    number: Optional[str]
    tense: Optional[str]
    proper: bool
    complex: bool

    __tablename__ = "real_words_FR"


class GeneratedWordEN(SQLModel, table=True):
    id: int = Field(primary_key=True)
    string: str
    type: Optional[str]
    number: Optional[str]
    tense: Optional[str]
    date: datetime
    ip: str

    __tablename__ = "generated_words_EN"


class GeneratedWordFR(SQLModel, table=True):
    id: int = Field(primary_key=True)
    string: str
    type: Optional[str]
    gender: Optional[str]
    number: Optional[str]
    tense: Optional[str]
    conjug: Optional[str]
    date: datetime
    ip: str

    __tablename__ = "generated_words_FR"


engine = create_engine(MYSQL_URL, echo=True)
