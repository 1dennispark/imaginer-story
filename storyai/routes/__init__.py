from fastapi import APIRouter

from . import persona, synopsis

root = APIRouter(prefix="/v1")
root.include_router(persona.router)
root.include_router(synopsis.router)