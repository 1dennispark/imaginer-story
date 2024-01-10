import functools
from typing import Annotated

import sqlalchemy
from fastapi import Depends
from sqlalchemy import orm

from . import services, completion
from .settings import Settings


@functools.cache
def settings() -> Settings:
    return Settings()


@functools.cache
def db_engine(settings: Annotated[Settings, Depends(settings)]):
    engine = sqlalchemy.create_engine(settings.mysql_url)
    try:
        yield engine
    finally:
        engine.dispose()


def db_session(engine: Annotated[sqlalchemy.engine.Engine, Depends(db_engine)]):
    session = orm.Session(engine)
    try:
        yield session
    finally:
        session.close()


def completer(
        settings: Annotated[Settings, Depends(settings)],
) -> completion.Completer:
    completer = completion.Completer(settings.openai_api_key, settings.completion_model)
    return completer


def persona_service(
        db: Annotated[orm.Session, Depends(db_session)],
        completer: Annotated[completion.Completer, Depends(completer)],
) -> services.PersonaService:
    persona_service = services.PersonaService(db, completer)
    return persona_service


def synopsis_service(
        db: Annotated[orm.Session, Depends(db_session)],
        completer: Annotated[completion.Completer, Depends(completer)],
) -> services.SynopsisService:
    synopsis = services.SynopsisService(db, completer)
    return synopsis
