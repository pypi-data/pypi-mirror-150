from __future__ import annotations

import os
from abc import ABC, abstractmethod
from enum import Enum, IntEnum
from typing import IO, Any, Callable, Iterable, Optional, Union

import boto3
from azure.core.exceptions import AzureError
from azure.storage.blob import (
    BlobClient,
    BlobProperties,
    ContainerClient,
    ContentSettings,
)
from botocore.exceptions import BotoCoreError, ClientError

from cloud_utils import exceptions

BotoError = (BotoCoreError, ClientError)


class StorageClass(IntEnum):
    STANDARD = 0
    INFREQUENT_ACCESS = 1
    ARCHIVE = 2


class StorageObject(ABC):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client

    @property
    @abstractmethod
    def path(self):
        pass

    @property
    @abstractmethod
    def bucket_name(self) -> str:
        pass

    @property
    @abstractmethod
    def content_length(self) -> int:
        pass

    @abstractmethod
    def exists(self) -> bool:
        pass

    @abstractmethod
    def download(self, stream: IO) -> None:
        pass

    @abstractmethod
    def upload(self, content: Iterable | IO, **kwargs: Any) -> None:
        pass

    @property
    def storage_class(self) -> str:
        provider_storage_cls = self._provider_storage_class
        try:
            return self.StorageClassMap[provider_storage_cls].value
        except KeyError:
            raise exceptions.UnsupportedStorageClassError(provider_storage_cls)

    def set_storage_class(self, storage_class: str) -> None:
        try:
            provider_storage_cls = self.StorageClassMap(storage_class).name
        except ValueError:
            raise exceptions.UnsupportedStorageClassError(storage_class)
        self._set_provider_storage_class(provider_storage_cls)

    @abstractmethod
    def _set_provider_storage_class(self, provider_storage_class: str) -> None:
        pass

    @property
    @abstractmethod
    def _provider_storage_class(self) -> str:
        pass

    class StorageClassMap(Enum):
        pass


class AmazonS3Object(StorageObject):
    @property
    def path(self):
        return self.client.key

    @property
    def bucket_name(self) -> str:
        return self.client.bucket_name

    @property
    def content_length(self) -> int:
        return self.client.content_length

    def exists(self) -> bool:
        try:
            self.client.load()
        except ClientError:
            return False
        else:
            return True

    def download(self, stream: IO) -> None:
        try:
            self.client.download_fileobj(stream)
        except BotoError as e:
            raise exceptions.StorageError(e)

    def upload(self, content: Iterable | IO, **kwargs: Any) -> None:
        content_type = kwargs.get("content_type")
        acl = kwargs.get("acl", "public-read")
        try:
            self.client.put(Body=content, ContentType=content_type, ACL=acl)
        except BotoError as e:
            raise exceptions.StorageError(e)

    @property
    def _provider_storage_class(self) -> str:
        return self.client.storage_class or "STANDARD"

    def _set_provider_storage_class(self, provider_storage_class: str) -> None:
        self.client.copy(
            {"Bucket": self.bucket_name, "Key": self.path},
            ExtraArgs={
                "StorageClass": provider_storage_class,
                "MetadataDirective": "COPY",
            },
        )

    class StorageClassMap(Enum):
        STANDARD = StorageClass.STANDARD.name
        ONEZONE_IA = StorageClass.INFREQUENT_ACCESS.name
        GLACIER = StorageClass.ARCHIVE.name


class AzureBlobObject(StorageObject):
    @property
    def path(self):
        return self.client.blob_name

    @property
    def bucket_name(self) -> str:
        return self.client.container_name

    @property
    def content_length(self) -> int:
        return self.client.get_blob_properties()["size"]

    def exists(self) -> bool:
        return self.client.exists()

    def download(self, stream: IO) -> None:
        try:
            self.client.download_blob().readinto(stream)
        except AzureError as e:
            raise exceptions.StorageError(e)

    def upload(self, content: Iterable | IO, **kwargs: Any) -> None:
        content_type = kwargs.get("content_type")
        content_settings = ContentSettings(content_type=content_type)
        try:
            self.client.upload_blob(
                content,
                overwrite=True,
                content_settings=content_settings,
            )
        except AzureError as e:
            raise exceptions.StorageError(e)

    @property
    def _provider_storage_class(self) -> str:
        return self.client.get_blob_properties()["blob_tier"]

    def _set_provider_storage_class(self, provider_storage_class: str) -> None:
        self.client.set_standard_blob_tier(provider_storage_class)

    class StorageClassMap(Enum):
        Hot = StorageClass.STANDARD.name
        Cool = StorageClass.INFREQUENT_ACCESS.name
        Archive = StorageClass.ARCHIVE.name


class Storage(ABC):
    object_class: type[StorageObject]

    def get_object(self, path: str) -> StorageObject:
        object_client = self.object_client_class(path)
        return self.object_class(object_client)

    @property
    @abstractmethod
    def object_client_class(self):
        pass


class AmazonS3Storage(Storage):
    object_class: type[StorageObject] = AmazonS3Object

    def __init__(self, bucket_name: str, region_name: str, **kwargs: Any) -> None:
        self.bucket_name: str = bucket_name
        self.region_name: str = region_name
        self.bucket = self._get_bucket(**kwargs)

    @property
    def object_client_class(self):
        return self.bucket.Object

    def _get_bucket(self, **kwargs: Any):
        aws_access_key_id = kwargs.get(
            "aws_access_key_id",
            os.environ.get("AWS_ACCESS_KEY_ID"),
        )
        aws_secret_access_key = kwargs.get(
            "aws_secret_access_key",
            os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )

        s3_kwargs = {"region_name": self.region_name}

        if aws_access_key_id and aws_secret_access_key:
            s3_kwargs["aws_access_key_id"] = aws_access_key_id
            s3_kwargs["aws_secret_access_key"] = aws_secret_access_key

        s3 = boto3.resource("s3", **kwargs)
        return s3.Bucket(self.bucket_name)


class AzureBlobStorage(Storage):
    object_class: type[StorageObject] = AzureBlobObject

    def __init__(self, container_name: str, **kwargs: Any) -> None:
        connection_string = kwargs.get(
            "conn_str",
            os.environ.get("AZURE_STORAGE_CONNECTION_STRING"),
        )
        self.client: ContainerClient = ContainerClient.from_connection_string(
            conn_str=connection_string, container_name=container_name
        )

    @property
    def object_client_class(
        self,
    ) -> Callable[[Union[str, BlobProperties], Optional[str]], BlobClient]:
        return self.client.get_blob_client
