# Copyright (c) Huawei Technologies Co., Ltd. 2023. All rights reserved.

from typing import Callable, Union
from dataclasses import dataclass


@dataclass
class StorageOptions:
    auto_retry: Union[bool, None] = None
    max_retries: Union[int, None] = None
    timeout: Union[int, None] = None


@dataclass
class GetFilesOptions:
    max_keys: Union[int, None] = None
    marker: Union[str, None] = None
    prefix: Union[str, None] = None
    delimiter: Union[str, None] = None


@dataclass
class DeleteFileOptions(GetFilesOptions):
    force_pause: Union[bool, None] = None


@dataclass
class DownloadOptions:
    destination: Union[str, None]


@dataclass
class SaveOptions:
    on_upload_progress: Union[Callable, None]
    size: Union[int, None]


@dataclass
class CreateWriteStreamOptions:
    size: int
    sha256: Union[str, None]
