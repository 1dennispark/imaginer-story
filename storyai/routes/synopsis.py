from typing import Annotated

from fastapi import APIRouter, Depends

from .. import models
from ..services import SynopsisService
from ..context import synopsis_service

router = APIRouter(prefix="/synopses")


@router.post("", response_model=models.Synopsis)
def add_synopsis(
        input: models.AddSynopsisInput,
        ss: Annotated[SynopsisService, Depends(synopsis_service)],
):
    synopsis = ss.add_synopsis(input)
    return synopsis


@router.get("", response_model=list[models.Synopsis])
def list_synopses(
        ss: Annotated[SynopsisService, Depends(synopsis_service)],
):
    synopses = ss.get_all_synopses()
    return synopses


@router.get("/{synopsis_id}", response_model=models.Synopsis)
def get_synopsis(
        synopsis_id: int,
        ss: Annotated[SynopsisService, Depends(synopsis_service)],
):
    synopsis = ss.get_synopsis(synopsis_id)
    return synopsis
