# Copyright (c) Huawei Technologies Co., Ltd. 2023. All rights reserved.

from typing import Optional

from agconnect.common_server.src.http_client.http_client_api import HttpMethod
from agconnect.cloud_storage.src.config.config import Config
from agconnect.cloud_storage.src.exception.agconnect_cloud_storage_exception import \
    convert_error_code, AGCCloudStorageException
from agconnect.cloud_storage.src.request.request import CRT_ERR, DNS_ERR, raw_request
from agconnect.common_server.src.log_config import logger


async def request(method_type: HttpMethod,
                  request_uri: str,
                  data: any,
                  request_params: any,
                  request_headers: any,
                  storage,
                  area: str,
                  type_: Optional[int] = None,
                  stream_res: Optional[bool] = None):
    """type of storage parameter must be of type StorageManagement"""
    auto_retry = storage.auto_retry
    max_retries = storage.max_retries

    if type_ is not None and type_ == 0:
        auto_retry = False
    first_time = True
    retry_time = 1
    last_request_domain = ''
    while first_time or (auto_retry and retry_time <= max_retries):
        url_info = await Config.get_instance(storage.name).get_storage_host(area)
        url = url_info.get('url') + request_uri
        last_time = retry_time == max_retries
        first_time = False
        try:
            res = await raw_request(method_type, url, data, request_params, request_headers, storage, stream_res)
            if res.status != 200:
                logger.error(res.reason)
                raise convert_error_code(res.status, res.status, res.reason)
            return res
        except (Exception, AGCCloudStorageException) as e:
            if getattr(e, 'errno', None) is not None and e.errno == 10013:
                err_headers = e.args[1]
                logger.warning('Cannot connect to server. Retrying...')
                strerror = err_headers.strerror if err_headers else None
                raise convert_error_code(e.errno, e.errno, strerror) from e

            if type_ is not None and type_ == 3 and getattr(e, 'errno', None) == 404:
                err_headers = e.args[1]
                raise convert_error_code(e.errno, e.errno, e.strerror if err_headers else None) from e

            error_exists = getattr(e, 'errno', None) is not None
            last_request_same_domain = last_request_domain == url_info.get('url')
            is_dns_error = e.errno in DNS_ERR or str(e.errno) in CRT_ERR

            if error_exists and last_request_same_domain and is_dns_error:
                await Config.get_instance(storage.name).set_storage_host(url_info, area)

            if not auto_retry:
                if getattr(e, 'errno', None) is not None:
                    err_headers = e.args[1] if len(e.args) > 1 else None
                    raise convert_error_code(e.errno,
                                             e.errno if err_headers else None,
                                             getattr(e, 'strerror', None)) from e
                elif isinstance(e, AGCCloudStorageException):
                    raise e

            else:
                logger.error(f'Request {retry_time} time/times failed.')
                retry_time += 1
                last_request_domain = url_info.get('url')
                if last_time:
                    if isinstance(e, AGCCloudStorageException):
                        raise e
                    else:
                        err_headers = e.args[1] if len(e.args) > 1 else None
                        if getattr(e, 'errno', None) is not None:
                            raise convert_error_code(getattr(e, 'errno', None),
                                                     getattr(e, 'errno', None) if err_headers else None,
                                                     getattr(e, 'strerror', None)) from e
                        else:
                            raise e


async def generate_res(request_res):
    try:
        return await request_res
    except Exception as e:
        raise e
