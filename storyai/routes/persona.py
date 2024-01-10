import logging
from typing import Annotated, Optional

import pydantic
from fastapi import APIRouter, Depends

from .. import models
from ..services import PersonaService
from ..context import persona_service

router = APIRouter(prefix="/personas")
logger = logging.getLogger(__name__)


@router.post("")
def create_persona(
        input: models.AddCharacterInput,
        ps: Annotated[PersonaService, Depends(persona_service)],
) -> None:
    persona = ps.add_character(input)
    logger.info(f'added persona ID: {persona.id}, context: {persona.context}')


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

