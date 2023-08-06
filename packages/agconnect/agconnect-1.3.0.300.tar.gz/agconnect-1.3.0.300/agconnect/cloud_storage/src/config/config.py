# Copyright (c) Huawei Technologies Co., Ltd. 2023. All rights reserved.

from __future__ import annotations

from typing import Dict, Callable, Optional
import os

import asyncio

from agconnect.cloud_storage.src.exception.agconnect_cloud_storage_exception import invalid_credential, \
    no_address_available
from agconnect.cloud_storage.src.model.models import AddressCount
from agconnect.common_server import AGCClient
from agconnect.common_server.src.config import ConfigService
from agconnect.common_server import logger

CLOUD_STORAGE = 'CloudStorage'


class AsyncLock:
    def __init__(self, timeout: int = 5000, max_pending: int = 1000):
        self.queue = asyncio.Queue()
        self.timeout = timeout
        self.max_pending = max_pending

    async def acquire(self, key: str, func: Callable):
        async with asyncio.Semaphore(self.max_pending):
            async with asyncio.Lock():
                while not self.queue.empty() and self.queue.get_nowait() != key:
                    pass
                self.queue.put_nowait(key)
                try:
                    return await asyncio.wait_for(func(), self.timeout)
                finally:
                    if not self.queue.empty():
                        self.queue.get_nowait()


lock = AsyncLock(5000, 1000)


class Config:
    INSTANCE_MAP: Dict[str: Config] = {}
    _default_region = None
    _url_info = {}
    _address_threshold = 3
    _time = 60000000
    _product_id: str
    _client_id: str
    _name: str

    def __init__(self, name: str):
        self._name = name
        self._product_id = AGCClient.get_instance(self._name).get_credential().get_project_id()
        self._client_id = AGCClient.get_instance(self._name).get_credential().get_client_id()
        region = AGCClient.get_instance(self._name).get_credential().get_region()
        if not region or region == '':
            logger.error('Get project region failed.')
            raise invalid_credential()
        self._default_region = region
        if not ConfigService.get_service(CLOUD_STORAGE).get_config_value('storage_url'):
            config_path = os.path.normpath(os.path.join(os.path.dirname(
                __file__), './../../agconnect_cloud_storage.json'))
            logger.info(config_path)
            ConfigService.initial_load_service_config("CLOUD_STORAGE", str(config_path))
        config = ConfigService.get_service(CLOUD_STORAGE).get_config_value('storage_url')
        for item in config:
            self._url_info[item["region"]] = {
                '0': {
                    'url': item["urlInfo"]["url"],
                    'index': 0,
                    'count': 0
                },
                '1': {
                    'url': item["urlInfo"]["url_back"],
                    'index': 1,
                    'count': 0
                }
            }

    @staticmethod
    def get_instance(name: str or None) -> Config:
        name = AGCClient.get_instance(name).get_name()
        if name not in Config.INSTANCE_MAP:
            Config.INSTANCE_MAP.update({'name': Config(name)})
        return Config.INSTANCE_MAP.get("name")

    async def get_storage_host(self, region: Optional[str]) -> AddressCount:
        region = region if region else self._default_region
        info: AddressCount
        return await lock.acquire(region, lambda: self.get_storage_host_func(region))

    async def get_storage_host_func(self, region):
        temp = self._url_info.get(region)
        for i in range(2):
            info: AddressCount = temp.get(str(i))
            if not info:
                raise no_address_available()
            if info.get("count") < self._address_threshold:
                return info
            elif i == 1:
                return info

    async def set_storage_host(self, address_count: AddressCount, region: str):
        region = region if region else self._default_region
        await lock.acquire(region, lambda: self.set_storage_host_func(address_count, region))
        return

    def set_storage_host_func(self, address_count: AddressCount, region: str):
        temp = self._url_info.get(region)
        index = address_count.get("index")
        try:
            temp[index] = temp.get(index) + 1
        except Exception as e:
            raise e from e
        self._url_info[region] = temp

    @property
    def default_region(self):
        return self._default_region

    @property
    def product_id(self):
        return self._product_id

    @property
    def client_id(self):
        return self._client_id
