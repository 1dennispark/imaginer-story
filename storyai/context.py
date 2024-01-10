import functools
import logging
from typing import Annotated

import oci.object_storage
import sqlalchemy
from fastapi import Depends
from oci.object_storage import ObjectStorageClient
from sqlalchemy import orm

from . import services, completion
from .settings import Settings


logger = logging.getLogger(__name__)
settings = Settings()


@functools.lru_cache()
def db_engine():
    return sqlalchemy.create_engine(settings.mysql_url)


def db_session(engine: Annotated[sqlalchemy.engine.Engine, Depends(db_engine)]):
    session = orm.Session(engine)
    try:
        yield session
    finally:
        session.close()


def completer() -> completion.Completer:
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


def oci_config() -> dict[str, str]:
    return {
        "user": settings.oci_user,
        "key_content": settings.oci_key,
        "fingerprint": settings.oci_fingerprint,
        "tenancy": settings.oci_tenancy,
        "region": settings.oci_region,
    }


def object_storage_client(
        conf: Annotated[dict[str, str], Depends(oci_config)],
):
    return oci.object_storage.ObjectStorageClient(conf)


def storage_service(
        client: Annotated[ObjectStorageClient, Depends(object_storage_client)],
):
    return services.ImageStorageService(
        client,
        settings.oci_bucket_namespace,
        settings.oci_bucket_name,
    )
