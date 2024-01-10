from datetime import datetime

import pydantic
from pydantic import ConfigDict

from . import domain


class AddCharacterInput(pydantic.BaseModel):
    name: str
    age: str
    gender: domain.Gender
    mbti: str
    description: str
    original_images: list[str]
    context: str | None = None
    profile_image: str | None = None


class Character(pydantic.BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

    name: str
    age: str
    mbti: str
    gender: domain.Gender
    description: str

    context: str
    profile_image: str
    original_images: list[str]


class GenerateSynopsisInput(pydantic.BaseModel):
    genre: str
    background: str
    ending: str
    character_ids: list[int]
    event_description: str


class SynopsisContent(pydantic.BaseModel):
    title: str
    detail: str


class GenerateScenarioInput(GenerateSynopsisInput):
    genre: str
    background: str
    ending: str
    character_ids: list[int]
    event_description: str
    synopses: list[SynopsisContent]


class Synopsis(pydantic.BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

    genre: str
    character_ids: list[int]
    background: str
    ending: str
    event_description: str

    contents: list[str]
    conversation: str | None


class GenerateCharacterInput(pydantic.BaseModel):
    name: str
    age: str
    mbti: str
    gender: domain.Gender
    description: str
    original_images: list[str]


class GenerateCharacterOutput(pydantic.BaseModel):
    context: str
    profile_image: str