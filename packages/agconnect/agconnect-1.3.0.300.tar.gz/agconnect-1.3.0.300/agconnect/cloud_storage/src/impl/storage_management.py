# Copyright (c) Huawei Technologies Co., Ltd. 2023. All rights reserved.

from dataclasses import dataclass
from typing import Optional, Union

import asyncio

from agconnect.common_server.src.http_client.http_client_api import HttpMethod
from agconnect.cloud_storage.src.impl.bucket import Bucket
from agconnect.cloud_storage.src.shared.request_with_storage_shared import generate_res, request
from agconnect.cloud_storage.src.model.callback import GetBucketsResponse, GetAllBucketsResponse, CreateBucketResponse
from agconnect.cloud_storage.src.shared.shared_dataclass_stream_file import BucketMetadata
from agconnect.cloud_storage.src.config.config import Config
from agconnect.cloud_storage.src.utils.validator import validate_bucket_name, validate_bucket_name_string, validate_area
from agconnect.cloud_storage.src.utils.common import random_string
from agconnect.cloud_storage.src.impl.constant import DEFAULT_AUTO_RETRY, DEFAULT_MAX_RETRIES, DEFAULT_TIME_OUT
from agconnect.common_server import AGCClient, AGCService


@dataclass
class StorageOptions:
    auto_retry: Union[bool, None] = None
    max_retries: Union[int, None] = None
    timeout: Union[int, None] = None


class StorageManagement(AGCService):
    _auto_retry: bool = DEFAULT_AUTO_RETRY
    _max_retries: int = DEFAULT_MAX_RETRIES
    _timeout: int = DEFAULT_TIME_OUT
    _name: Optional[str] = None

    def __init__(self, options: Optional[StorageOptions] = None):
        if options and options.auto_retry is not None:
            self.auto_retry = options.auto_retry
        if options and options.max_retries is not None:
            self.max_retries = options.max_retries
        if options and options.timeout is not None:
            self.timeout = options.timeout

    def bucket(self, name: str, area: Optional[str] = None) -> "Bucket":
        validate_bucket_name_string('storage.bucket: ', name)
        if area:
            validate_area('storage.bucket: ', area)
        return Bucket(self, name, area)

    async def create_bucket(self, name: str, area: Optional[str] = None,
                            metadata: BucketMetadata = None) -> CreateBucketResponse:
        area = area if type(area) == str else Config.get_instance(self._name).default_region
        metadata = area if type(area) == object else metadata
        validate_bucket_name('storage.create_bucket: ', name)
        validate_area('storage.create_bucket: ', area)
        url = '/v0/'
        headers = {
            'X-Agc-Bucket-Name': name + '-' + random_string(5)
        }
        data = None
        if metadata and metadata.cors:
            data = {
                'rules': metadata.cors
            }
        return await generate_res(request(method_type=HttpMethod.PUT, request_uri=url, data=data, request_params=None,
                                          request_headers=headers, storage=self, area=area))

    async def get_buckets(self, area: Optional[str] = None) -> GetBucketsResponse:
        area = area if area else Config.get_instance(self._name).default_region
        validate_area('storage.get_buckets: ', area)
        url = '/v0/'
        header = {}
        return await generate_res(request(HttpMethod.GET, url, None, None, header, self, area))

    async def get_all_buckets(self) -> GetAllBucketsResponse.GetAllBucketsResponse:
        regions = ["CN", "RU", "DE", "SG"]
        result: GetAllBucketsResponse.GetAllBucketsResponse = {}

        async def query_buckets(region: str):
            try:
                res = await self.get_buckets(region)
                result[region] = res
            except Exception:
                result[region] = None
            return result

        limit = asyncio.Semaphore(10)

        async def func(region):
            async with limit:
                res = await query_buckets(region)
                return res

        tasks = [func(region) for region in regions]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            result.update(response)
        return result

    @property
    def auto_retry(self) -> bool:
        return self._auto_retry

    @auto_retry.setter
    def auto_retry(self, value: bool):
        self._auto_retry = value

    @property
    def max_retries(self):
        return self._max_retries

    @max_retries.setter
    def max_retries(self, value: int):
        self._max_retries = value

    @property
    def timeout(self) -> int:
        return self._timeout

    @timeout.setter
    def timeout(self, value: int):
        self._timeout = value

    def get_service_name(self) -> str:
        return "CloudStorage"

    def initialize(self, client: AGCClient):
        self._name = client.get_name()

    @property
    def name(self) -> str or None:
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
