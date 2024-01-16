from datetime import datetime

import pydantic
from pydantic import ConfigDict

from . import domain


class Character(pydantic.BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    name: str
    age: str
    mbti: str
    job: str
    gender: domain.Gender
    description: str

    context: str
    profile_image: str | None
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


class AddCharacterInput(pydantic.BaseModel):
    name: str
    age: str
    mbti: str
    gender: domain.Gender
    description: str
    job: str
    original_images: list[str]


class ProfileImage(pydantic.BaseModel):
    object_name: str | None
    status: str
