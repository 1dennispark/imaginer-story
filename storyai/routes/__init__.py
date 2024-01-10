from fastapi import APIRouter

from . import persona, synopsis, images

root = APIRouter(prefix="/v1")
root.include_router(persona.router)
root.include_router(synopsis.router)
root.include_router(images.router)