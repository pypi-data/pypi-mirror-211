# Copyright (c) Huawei Technologies Co., Ltd. 2023. All rights reserved.

from dataclasses import dataclass
from typing import Callable, Optional, Any

import uuid
import urllib.parse
from tqdm import tqdm

from agconnect.cloud_storage.src.upload.file_stream import FileReader
from agconnect.common_server.src.http_client.http_client_api import HttpMethod
from agconnect.cloud_storage.src.config.config import Config
from agconnect.cloud_storage.src.exception.agconnect_cloud_storage_exception import AGCCloudStorageException
from agconnect.cloud_storage.src.upload.fetch import fetch
from agconnect.cloud_storage.src.request.request import generate_auth
from agconnect.common_server import AGCClient


@dataclass
class ResumableUploadOpt:
    bucket: Any
    file: Any
    size: int
    storage: Any
    area: str
    offset: int
    upload_size: int
    metadata: Any = None
    sha256: str = None
    on_upload_progress: Optional[Callable[[Any], None]] = None


@dataclass
class OffsetOpt:
    size: int
    sha256: str
    bucket: Any
    file: Any


async def get_offset(options: OffsetOpt, bucket: Any) -> Any:
    url_info = await Config.get_instance(bucket.storage.name).get_storage_host(bucket.area)
    url = url_info.get("url") + '/v0/' + options.bucket.name + '/' + urllib.parse.quote(options.file.name)
    token = await generate_auth(AGCClient.get_instance(options.bucket.storage.name))
    headers = {
        'X-Agc-Upload-Protocol': 'resumable',
        'X-Agc-File-Size': str(options.size),
        'X-Agc-Sha256': options.sha256,
        'Authorization': token,
        'client_id': Config.get_instance(options.bucket.storage.name).client_id,
        'productId': Config.get_instance(options.bucket.storage.name).product_id,
        'X-Agc-Trace-Id': str(uuid.uuid1()),
    }
    response = await fetch(url, HttpMethod.POST, data=None, headers=headers)
    return response


class ResumableUpload:
    def __init__(self, opt: ResumableUploadOpt):
        self.bucket = opt.bucket
        self.file = opt.file
        self.metadata = opt.metadata
        self.sha256 = opt.sha256
        self.size = opt.size
        self.area = opt.area
        self.storage = opt.storage
        self.upload_size = opt.upload_size
        self.offset = opt.offset

    async def upload(self, file_path, on_upload_progress: Callable) -> Any:
        with open(file_path, 'rb') as file_obj:
            offset = 0
            upload_obj = FileReader(file_obj, file_path, on_progress=on_upload_progress)
            tqdm_ = tqdm(total=upload_obj.total_size, unit='B', unit_scale=True, unit_divisor=1024,
                         desc="Uploading", colour='green', ncols=100)
            async for chunk in upload_obj.generate_chunks():
                try:
                    resp = await self.upload_request(data=chunk, offset=offset)
                    tqdm_.update(len(chunk))
                    offset += len(chunk)
                except (AGCCloudStorageException, Exception) as e:
                    raise e
            return resp

    async def upload_request(self, data, offset=None) -> Any:
        url = '/v0/' + self.bucket.name + '/' + urllib.parse.quote(self.file.name)
        headers = {
            'X-Agc-File-Size': str(self.size),
            'X-Agc-File-Offset': str(self.offset)
        }
        if offset is not None:
            headers['X-Agc-File-Offset'] = str(offset)
        if self.sha256:
            headers['X-Agc-Sha256'] = self.sha256
        try:
            auth = await generate_auth(AGCClient.get_instance(self.storage.name))
            auth_header = {
                'Authorization': auth,
                'client_id': Config.get_instance(self.storage.name).client_id,
                'productId': Config.get_instance(self.storage.name).product_id,
                'X-Agc-Trace-Id': str(uuid.uuid1()),
                'Content-Type': 'application/octet-stream'
            }
            url_info = await Config.get_instance(self.storage.name).get_storage_host(self.bucket.area)
            uri = url_info.get("url") + url
            headers.update(auth_header)
            response = await fetch(uri, HttpMethod.PUT, data=data, headers=headers)
            return response
        except (Exception, AGCCloudStorageException) as e:
            raise Exception("Request failed", e) from e
