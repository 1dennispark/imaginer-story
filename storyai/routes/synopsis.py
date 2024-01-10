from typing import Annotated

from fastapi import APIRouter, Depends

from .. import models
from ..services import SynopsisService
from ..context import synopsis_service

router = APIRouter(prefix="/synopses")


@router.post("")
def generate_synopsis(
        input: models.GenerateSynopsisInput,
        ss: Annotated[SynopsisService, Depends(synopsis_service)],
):
    return ss.generate_synopsis(input)


@router.post("/scenario")
def generate_scenario(
        input: models.GenerateScenarioInput,
        ss: Annotated[SynopsisService, Depends(synopsis_service)],
):
    return ss.generate_scenario(input)
