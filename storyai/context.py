import functools
import grpc
import logging
from typing import Annotated

import oci.object_storage
import sqlalchemy
from fastapi import Depends
from oci.object_storage import ObjectStorageClient
from sqlalchemy import orm

from . import completion, proto
from .services import DreamBoothService, ImageStorageService, SynopsisService, PersonaService
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


def synopsis_service(
        db: Annotated[orm.Session, Depends(db_session)],
        completer: Annotated[completion.Completer, Depends(completer)],
) -> SynopsisService:
    synopsis = SynopsisService(db, completer)
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
    return ImageStorageService(
        client,
        settings.oci_bucket_namespace,
        settings.oci_bucket_name,
    )


def dreambooth_controller():
    with grpc.insecure_channel(settings.paugen_dreambooth_controller_target) as channel:
        yield proto.DreamBoothControllerStub(channel)


def diffuser():
    with grpc.insecure_channel(settings.paugen_diffuser_target) as channel:
        yield proto.DiffuserStub(channel)


def dreambooth_service(
        ctrl: Annotated[proto.DreamBoothControllerStub, Depends(dreambooth_controller)],
        diffuser: Annotated[proto.DiffuserStub, Depends(diffuser)],
        db: Annotated[orm.Session, Depends(db_session)],
):
    return DreamBoothService(
        db=db,
        settings=settings,
        ctrl=ctrl,
        diffuser=diffuser,
    )


def persona_service(
        db: Annotated[orm.Session, Depends(db_session)],
        completer: Annotated[completion.Completer, Depends(completer)],
        dreambooth_service: Annotated[DreamBoothService, Depends(dreambooth_service)],
        storage_service: Annotated[ImageStorageService, Depends(storage_service)],
) -> PersonaService:
    return PersonaService(
        db, completer, dreambooth_service,
        storage_service,
    )
