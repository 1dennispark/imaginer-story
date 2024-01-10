import enum
from datetime import datetime

from sqlalchemy import func, String, ForeignKey, TEXT
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
    age: Mapped[int] = mapped_column(nullable=False)
    mbti: Mapped[str] = mapped_column(String(8), nullable=False)
    gender: Mapped[Gender] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(TEXT, nullable=False)

    context: Mapped[str] = mapped_column(TEXT, nullable=True)


class Synopsis(Base):
    __tablename__ = 'synopses'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    theme: Mapped[str] = mapped_column(String(256), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey("personas.id"), nullable=False)
    character: Mapped[Persona] = relationship(foreign_keys=[character_id])

    content: Mapped[str] = mapped_column(TEXT, nullable=False)
