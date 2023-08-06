# Copyright (c) Huawei Technologies Co., Ltd. 2023. All rights reserved.

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Cors:
    origins: List[str]
    methods: List[str]
    headers: List[str]
    max_age_seconds: Optional[int] = None
    expose_headers: Optional[List[str]] = None


@dataclass
class BucketMetadata:
    cors: Optional[List[Cors]] = None


@dataclass
class CreateBucketResponse:
    bucket: str
    storage_area: str
    storage_type: str
    product_id: str
    storage_region: str
    creation_date: str


@dataclass
class GetCorsResponse:
    product_id: str
    bucket: str
    rules: List[Cors]
