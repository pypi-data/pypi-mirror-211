# Copyright (c) Huawei Technologies Co., Ltd. 2023. All rights reserved.

from dataclasses import dataclass
from typing import List, Union, Any, Dict


@dataclass
class CreateBucketResponse:
    bucket: str
    storage_area: str
    storage_type: str
    product_id: str
    storage_region: str
    creation_date: str


BucketExistResponse = bool


@dataclass
class Metadata:
    content_type: str
    cache_control: str = None
    content_disposition: str = None
    content_encoding: str = None
    content_language: str = None
    custom_metadata: Dict[str, str] = None


DownloadResponse = bytes
GetFileMetadataResponse = Metadata
MoveResponse = List[Any]
SetFileMetadataResponse = Metadata


@dataclass()
class FileExistResponse:
    exists: bool


@dataclass
class BucketDetail:
    bucket_name: str
    storage_area: str
    storage_region: str
    storage_type: str
    creation_date: str
    bucket_type: Union[str, None]


@dataclass
class GetBucketsResponse:
    product_id: str
    buckets: List[BucketDetail]


@dataclass
class GetAllBucketsResponse:
    GetAllBucketsResponse = Dict[str, Union[GetBucketsResponse, None]]
