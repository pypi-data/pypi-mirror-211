# Copyright (c) Huawei Technologies Co., Ltd. 2023. All rights reserved.

from typing import Optional
from dataclasses import dataclass


@dataclass
class StorageResponse:
    code: str
    message: str


AddressCount = {
    "url": str,
    "index": int,
    "count": int
}


@dataclass
class BucketDetail:
    bucket_name: str
    storage_area: str
    storage_region: str
    storage_type: str
    creation_date: str
    bucket_type: Optional[str] = None
