import enum
from datetime import datetime

from sqlalchemy import func, String, ForeignKey, TEXT, JSON, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Gender(enum.Enum):
    MALE = "남자"
    FEMALE = "여자"

    @classmethod
    def from_str(cls, value: str) -> 'Gender':
        value = value.lower()
        if value == 'male' or value == '남자':
            return Gender.MALE
        elif value == 'female' or value == '여자':
            return Gender.FEMALE
        else:
            raise RuntimeError("Gender is wrong")


class Persona(Base):
    __tablename__ = 'personas'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[str] = mapped_column(String(32), nullable=False)
    mbti: Mapped[str] = mapped_column(String(8), nullable=False)
    gender: Mapped[Gender] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(TEXT, nullable=False)
    job: Mapped[str] = mapped_column(String(32), nullable=False)

    profile_image: Mapped[str|None] = mapped_column(String(256), nullable=True)
    original_images: Mapped[list[str]|None] = mapped_column(JSON, nullable=True)
    context: Mapped[str|None] = mapped_column(TEXT, nullable=True)

    booth_id: Mapped[int|None] = mapped_column(nullable=True)


synopses_characters = Table(
    "synopses_characters",
    Base.metadata,
    Column("synopsis_id", ForeignKey("synopses.id"), primary_key=True),
    Column("persona_id", ForeignKey("personas.id"), primary_key=True),
)


class Synopsis(Base):
    __tablename__ = 'synopses'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    genre: Mapped[str] = mapped_column(String(32))
    background: Mapped[str] = mapped_column(String(32))
    ending: Mapped[str] = mapped_column(String(32))
    event_description: Mapped[str] = mapped_column(TEXT)

    characters: Mapped[list[Persona]] = relationship(secondary=synopses_characters)

    contents: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    conversation: Mapped[str] = mapped_column(TEXT, nullable=True)


class Prompt(Base):
    __tablename__ = 'prompts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    job: Mapped[str] = mapped_column(TEXT)
    male_prompt: Mapped[str] = mapped_column(TEXT)
    female_prompt: Mapped[str] = mapped_column(TEXT)
    negative_prompt: Mapped[str] = mapped_column(TEXT)