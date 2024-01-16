import httpx
import oci
import uuid

from typing import BinaryIO

from oci.object_storage import ObjectStorageClient


class ImageStorageService:
    def __init__(
            self,
            client: ObjectStorageClient,
            namespace: str,
            bucket: str,
    ):
        self._client = client
        self._ns = namespace
        self._bucket = bucket
        self._prefix = 'images/'

    def store(self, body: BinaryIO, content_type: str, ext: str = '') -> (str, str):
        object_name = uuid.uuid4().hex

        if ext != '':
            object_name += ext

        resp = self._client.put_object(
            namespace_name=self._ns,
            bucket_name=self._bucket,
            object_name=self._prefix + object_name,
            put_object_body=body,
            content_type=content_type,
        )

        return object_name, resp.headers['etag']

    def load(self, object_name, etag: str = '') -> (httpx.Response | None, str|None, str | None):
        try:
            resp = self._client.get_object(
                namespace_name=self._ns,
                bucket_name=self._bucket,
                object_name=self._prefix + object_name,
                if_none_match=etag,
            )

            content_type = resp.headers['content-type']
            etag = resp.headers['etag']

            return resp.data, content_type, etag
        except oci.exceptions.ServiceError as e:
            if e.status == 304:
                return None, None, None
            raise

    def remove(self, object_name: str) -> None:
        resp = self._client.delete_object(
            namespace_name=self._ns,
            bucket_name=self._bucket,
            object_name=self._prefix + object_name,
        )

        resp.data.raise_for_status()

