# Copyright (c) Huawei Technologies Co., Ltd. 2023. All rights reserved.

from __future__ import annotations

import asyncio
import os

from tqdm import tqdm
import re
from dataclasses import dataclass
import threading
from typing import Any, Optional, Union, Callable, List
import urllib.parse

from agconnect.cloud_storage.src.exception.agconnect_cloud_storage_exception import invalid_destination, \
    parse_destination_string_error, AGCCloudStorageException
from agconnect.cloud_storage.src.impl import storage_management, bucket
from agconnect.cloud_storage.src.utils.common import generate_path
from agconnect.common_server.src.http_client.http_client_api import HttpMethod
from agconnect.cloud_storage.src.model.callback import Metadata, FileExistResponse, \
    GetFileMetadataResponse, SetFileMetadataResponse, MoveResponse
from agconnect.cloud_storage.src.model.options import CreateWriteStreamOptions
from agconnect.cloud_storage.src.shared.request_with_storage_shared import generate_res, request
from agconnect.cloud_storage.src.utils.validator import validate_meta_data_opt, validate_not_null, \
    validate_destination_string, validate_bucket_name_string
from agconnect.common_server import logger

DES_REGEX = r'^([a-z0-9-]+)\/(.+)$'


@dataclass
class SimpleUploadOptions(CreateWriteStreamOptions):
    file: File


@dataclass
class GetFilesResponse:
    dirList: List[str]
    fileList: List[File]
    marker: Union[str, None] = None


@dataclass
class UploadOptions:
    destination: Union[str, File]
    on_upload_progress: Callable
    sha256: Union[str, None]


class File:
    storage: storage_management.StorageManagement
    name: str
    metadata: Metadata

    def __init__(self, bucket_obj: bucket.Bucket, name: str):
        validate_not_null(bucket_obj, "Bucket")
        self.bucket = bucket_obj
        self.name = generate_path(name)
        self.storage = bucket_obj.storage

    async def copy(self, des) -> [File]:
        des_bucket: str
        des_name: str
        new_file: Optional[File] = None
        if isinstance(des, str):
            validate_destination_string('', des)
            parsed_des = re.match(DES_REGEX, des)
            if parsed_des is not None and len(parsed_des.groups()) == 2:
                des_bucket = parsed_des.group(1)
                des_name = parsed_des.group(2)
            else:
                raise parse_destination_string_error()
        elif isinstance(des, bucket.Bucket):
            validate_bucket_name_string('', des.name)
            des_bucket = des.name
            des_name = self.name
        elif isinstance(des, File):
            des_bucket = des.bucket.name
            des_name = des.name
            new_file = des
        else:
            raise invalid_destination('')
        new_file = new_file or self.bucket.file(des_name)
        url = f"/v0/{des_bucket}/{urllib.parse.quote(des_name)}"
        headers = {
            'X-Agc-Copy-Source': f"/{urllib.parse.quote(self.name)}"
        }
        try:
            await generate_res(request(HttpMethod.PUT, url, None, None, headers, self.storage,
                                       self.bucket.area))
            return [new_file]
        except AGCCloudStorageException as err:
            logger.error("Error copy file", err)
            raise AGCCloudStorageException(err.get_message(), err.get_code()) from err

    async def download(self, local_file, on_download_progress: Callable):
        url = '/v0/' + self.bucket.name + '/' + urllib.parse.quote(self.name)
        header = {}
        try:
            async with await request(HttpMethod.GET, url, None, None, header, self.storage,
                                     self.bucket.area, 0, True) as res:
                total_size = res.content.total_bytes
                tqdm_ = tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024,
                             desc="Downloading", colour='green', ncols=100)
                fd = os.open(local_file, os.O_WRONLY | os.O_CREAT, 0o755)
                with os.fdopen(fd, 'wb') as f:
                    amount_seen = 0
                    async for chunk in res.content.iter_chunked(4 * 1024 * 1024):
                        f.write(chunk)
                        amount_seen += len(chunk)
                        tqdm_.update(len(chunk))
                        if on_download_progress:
                            if asyncio.iscoroutinefunction(on_download_progress):
                                progress = {'writtenBytes': amount_seen, 'totalBytes': total_size}
                                asyncio.create_task(on_download_progress(progress))
                            else:
                                progress = {'writtenBytes': amount_seen, 'totalBytes': total_size}
                                thread = threading.Thread(target=on_download_progress,
                                                          args=(progress,), daemon=True)
                                thread.start()
                res.close()
                return "File downloaded successfully. ", res
        except (Exception, AGCCloudStorageException) as e:
            logger.error("Error processing", e)
            return e, None

    async def delete(self):
        url = '/v0/' + self.bucket.name + '/' + urllib.parse.quote(self.name)
        headers = {}
        res = await generate_res(request(HttpMethod.DELETE, url, None, None, headers, self.storage,
                                         self.bucket.area))
        return res

    async def exists(self) -> FileExistResponse:
        url = '/v0/' + self.bucket.name + '/' + urllib.parse.quote(self.name) + '?metadata=query'
        headers = {}
        try:
            await request(HttpMethod.GET, url, None, None, headers, self.storage, self.bucket.area, 0)
            return FileExistResponse(True)
        except (AGCCloudStorageException, Exception) as err:
            if err.get_code() == '20013':
                return FileExistResponse(False)
            else:
                logger.error('FileExistResponse', err)
                return FileExistResponse(False)

    async def get(self) -> Union[File, Any]:
        url = '/v0/' + self.bucket.name + '/' + urllib.parse.quote(self.name)
        headers = {}
        try:
            res = await generate_res(request(HttpMethod.GET, url, None, None, headers, self.storage,
                                             self.bucket.area, 0))
            return res
        except (AGCCloudStorageException, Exception) as err:
            logger.error("Error GetFileResponse", err)
            raise AGCCloudStorageException(err.get_message(), err.get_code()) from err

    async def get_metadata(self) -> GetFileMetadataResponse:
        url = '/v0/' + self.bucket.name + '/' + urllib.parse.quote(self.name) + '?metadata=query'
        headers = {}
        return await generate_res(request(HttpMethod.GET, url, None, None, headers, self.storage,
                                          self.bucket.area))

    async def set_metadata(self, metadata: Metadata) -> SetFileMetadataResponse:
        validate_meta_data_opt('file.setMetadata', self.name)
        url = '/v0/' + self.bucket.name + '/' + urllib.parse.quote(self.name) + '?metadata=update'
        headers = {}
        if metadata.cache_control:
            headers['X-Agc-Cache-Control'] = metadata.cache_control
        if metadata.content_disposition:
            headers['X-Agc-Content-Disposition'] = metadata.content_disposition
        if metadata.content_encoding:
            headers['X-Agc-Content-Encoding'] = metadata.content_encoding
        if metadata.content_language:
            headers['X-Agc-Content-Language'] = metadata.content_language
        if metadata.content_type:
            headers['X-Agc-Content-Type'] = metadata.content_type
        if metadata.custom_metadata:
            for key, value in metadata.custom_metadata.items():
                header_name = f'X-Agc-meta-{key}'
                headers[header_name] = urllib.parse.quote(value)
        return await generate_res(request(HttpMethod.GET, url, None, None, headers, self.storage,
                                          self.bucket.area))

    async def move(self, des) -> MoveResponse:
        try:
            res = await self.copy(des)
            if res and res[0] and not (self.name == res[0].name and
                                       self.bucket.name == res[0].bucket.name):
                res_data = res[0]
                await self.delete()
                return [res_data]
            raise ValueError('new_file is None')
        except (AGCCloudStorageException, Exception) as err:
            logger.error("Error moving file", err)
            raise AGCCloudStorageException(err.get_message(), err.get_code()) from err
