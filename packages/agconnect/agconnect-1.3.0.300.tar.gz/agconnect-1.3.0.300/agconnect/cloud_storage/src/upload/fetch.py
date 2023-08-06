# Copyright (c) Huawei Technologies Co., Ltd. 2023. All rights reserved.

import json
from typing import Optional

from aiohttp import ClientTimeout

from agconnect.cloud_storage.src.request.request import get_storage_http_client
from agconnect.cloud_storage.src.utils.common import is_json_string
from agconnect.cloud_storage.src.exception.agconnect_cloud_storage_exception import convert_error_code
from agconnect.common_server.src.http_client.http_client_api import HttpMethod, HttpClientCfg
from agconnect.cloud_storage.src.impl.constant import DEFAULT_TIME_OUT
from agconnect.common_server import logger


async def fetch(uri: str, method: HttpMethod, data=Optional[None], headers=None):
    http_client_config = HttpClientCfg(
        is_enable_ssl_cert=True,
        timeout=ClientTimeout(DEFAULT_TIME_OUT),
    )
    try:
        http_client = get_storage_http_client(http_client_config)
        async with http_client as client:
            res = await client.request(method, uri, data=data, headers=headers)
        if res is None:
            convert_error_code(status_code=0, ret_code=0, data='')
        data = await res.text()
        if res.status != 200:
            convert_error_code(res.status, res.headers.get('error-code'), data)
            return
        if is_json_string(data):
            return json.loads(data)
        else:
            return data
    except Exception as e:
        logger.error('Error fetch', e)
        raise e
