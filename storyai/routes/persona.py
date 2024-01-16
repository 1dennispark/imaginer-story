import logging
from typing import Annotated, Optional

import pydantic
from fastapi import APIRouter, Depends

from .. import models
from ..services import PersonaService
from ..context import persona_service

router = APIRouter(prefix="/personas")
logger = logging.getLogger(__name__)


@router.post("", response_model=models.Character)
def add_persona(
        input: models.AddCharacterInput,
        ps: Annotated[PersonaService, Depends(persona_service)],
):
    persona = ps.save_character(None, input)
    logger.info(f'added persona ID: {persona.id}, context: {persona.context}')
    return persona


@router.put("/{id}", response_model=models.Character)
def update_character(
        id: int,
        input: models.AddCharacterInput,
        ps: Annotated[PersonaService, Depends(persona_service)],
):
    return ps.save_character(id, input)


@router.get("", response_model=list[models.Character])
def list_personas(
        ps: Annotated[PersonaService, Depends(persona_service)],
):
    personas = ps.get_all_characters()
    return personas


@router.get("/{persona_id}", response_model=models.Character)
def get_persona(
        persona_id: int,
        ps: Annotated[PersonaService, Depends(persona_service)],
):
    persona = ps.get_character(persona_id)
    return persona


@router.get("/{persona_id}/profile-image", response_model=models.ProfileImage)
def get_profile_image(
        persona_id: int,
        ps: Annotated[PersonaService, Depends(persona_service)],
):
    return ps.get_profile_image(persona_id)
