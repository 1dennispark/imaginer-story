from datetime import datetime

import pydantic

from . import domain


class AddCharacterInput(pydantic.BaseModel):
    name: str
    age: int
    gender: domain.Gender
    mbti: str
    description: str


class Character(pydantic.BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    name: str
    age: int
    mbti: str
    gender: domain.Gender
    description: str

    context: str


class AddSynopsisInput(pydantic.BaseModel):
    theme: str
    character_id: int


class Synopsis(pydantic.BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    theme: str
    character_id: str

    content: str
