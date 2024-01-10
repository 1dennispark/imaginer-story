from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Depends, Header
from fastapi.responses import FileResponse, Response, StreamingResponse

from .. import services, context

router = APIRouter(prefix="/images")


@router.post("")
def create_file(
        ss: Annotated[services.ImageStorageService, Depends(context.storage_service)],
        image: UploadFile = File(),
):
    ext = image.filename[image.filename.rfind('.'):]
    object_name, etag = ss.store(image.file, content_type=image.content_type, ext=ext)
    return {'object_name': object_name, 'etag': etag}


@router.get("/{object_name}")
def get_file(
        object_name: str,
        ss: Annotated[services.ImageStorageService, Depends(context.storage_service)],
        if_none_match: str = Header(default=''),
):
    body, content_type, etag = ss.load(object_name, etag=if_none_match)
    if etag is None:
        return Response(status_code=304, headers={'ETag': if_none_match})
    else:
        return StreamingResponse(content=body.iter_content(chunk_size=4096), media_type=content_type, headers={'ETag': etag})


@router.delete("/{object_name}")
def delete_file(
        object_name: str,
        ss: Annotated[services.ImageStorageService, Depends(context.storage_service)],
):
    ss.remove(object_name)
