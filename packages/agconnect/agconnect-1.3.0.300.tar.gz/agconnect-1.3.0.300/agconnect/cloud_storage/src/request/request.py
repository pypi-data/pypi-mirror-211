# Copyright (c) Huawei Technologies Co., Ltd. 2023. All rights reserved.

import json
import uuid
from types import TracebackType
from typing import Optional, Type

from aiohttp import ClientTimeout
from dns import rcode

from agconnect.common_server.src.error import AGCException, ErrorCodeConstant
from agconnect.common_server import logger
from agconnect.cloud_storage.src.config.config import Config
from agconnect.cloud_storage.src.impl.constant import DEFAULT_MAX_BODY_LENGTH
from agconnect.cloud_storage.src.exception.agconnect_cloud_storage_exception import generate_token_error
from agconnect.common_server import AGCClient
from agconnect.common_server.src.http_client import CommonHeaders
from agconnect.common_server.src.http_client.http_client_api import HttpMethod, HttpClientCfg, HttpClientApiImpl
from agconnect.common_server.src.utils.utils import url_validate

from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Union, AsyncIterator


def get_storage_http_client(cfg: Union[HttpClientCfg, dict] = None):
    if type(cfg) is dict:
        return Root(HttpClientCfg(dictionary=cfg)).client()
    return Root(cfg).client()


@dataclass(frozen=True)
class Root:
    cfg: Union[HttpClientCfg, dict]

    @asynccontextmanager
    async def client(self) -> AsyncIterator[HttpClientApiImpl]:
        client = CloudStorageHttpClientApiImpl(self.cfg)
        try:
            yield client
        except AGCException as e:
            raise e
        finally:
            await client.close()


class CloudStorageHttpClientApiImpl(HttpClientApiImpl):
    async def __aenter__(self) -> "HttpClientApiImpl":
        return self

    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
    ) -> Optional[bool]:
        await self.close()
        return None

    def __init__(self, cfg: HttpClientCfg):
        cfg.proxy_map = cfg.proxy_map or {}
        self.__proxy_map = cfg.proxy_map
        self.__sslcontext = None
        self.__resp_headers = {'User-Agent': CommonHeaders.get_user_agent(),
                               'serverSdkName': CommonHeaders.get_sdk_name(),
                               'serverSdkVersion': CommonHeaders.get_sdk_version(),
                               'X-Request-Id': CommonHeaders.generate_request_id()}
        super().__init__(cfg)
        self.__cli_sess = super().get_cli_sess()

    def request(self,
                method_type: HttpMethod,
                url: str,
                data=None,
                **options):
        if not url_validate(url):
            raise AGCException(ErrorCodeConstant.URL_VALIDATE_FAIL)
        headers = options.get("headers")
        if headers is None:
            headers = {}
        params = options.get("params")
        if params is None:
            params = {}
        proxy = options.get("proxy")
        proxy_auth = options.get("proxy_auth")
        if proxy is None:
            if self.__proxy_map.get("proxy_host"):
                proxy = self.__proxy_map.get("proxy_host")
            if self.__proxy_map.get("proxy_auth"):
                proxy_auth = self.__proxy_map.get("proxy_auth")
        return self.__cli_sess.request(str(method_type.value),
                                       url,
                                       data=data,
                                       headers=headers,
                                       params=params,
                                       proxy=proxy,
                                       proxy_auth=proxy_auth,
                                       ssl=self.__sslcontext)


async def generate_auth(agc_client: AGCClient):
    try:
        data = await agc_client.get_credential().get_access_token()
        token = data
    except Exception as e:
        logger.error("Error generate_auth", e)
        token = ''
    if token == '':
        logger.error('refresh token failed')
        raise generate_token_error()
    return 'Bearer ' + token


async def raw_request(method_type: HttpMethod,
                      request_uri: str,
                      data: any,
                      request_params: any,
                      request_headers: any,
                      storage,
                      stream_res: Optional[bool] = None):
    auth = await generate_auth(AGCClient.get_instance(storage.name))
    auth_header = {
        'Authorization': auth,
        'client_id': Config.get_instance(storage.name).client_id,
        'productId': Config.get_instance(storage.name).product_id,
        'X-Agc-Trace-Id': str(uuid.uuid1()),
    }
    auth_header.update(request_headers)
    header = auth_header
    timeout = storage.timeout
    if data:
        data = json.dumps(data)
    http_client_config = HttpClientCfg(
        timeout=ClientTimeout(timeout),
        max_body_length=DEFAULT_MAX_BODY_LENGTH,
        response_type="stream" if stream_res else None
    )

    http_client = get_storage_http_client(http_client_config)
    async with http_client as http_client:
        if method_type == HttpMethod.GET:
            return await http_client.request(
                HttpMethod.GET, request_uri, params=request_params, headers=header)
        elif method_type == HttpMethod.POST:
            return await http_client.request(
                HttpMethod.POST, request_uri, data=data, params=request_params, headers=header)
        elif method_type == HttpMethod.PUT:
            return await http_client.request(
                HttpMethod.PUT, request_uri, data=data, params=request_params, headers=header)
        elif method_type == HttpMethod.DELETE:
            return await http_client.request(
                HttpMethod.DELETE, request_uri, params=request_params, headers=header)
        else:
            logger.error('unsupported request method')
            return None


DNS_ERR: list = [rcode.NOERROR, rcode.FORMERR, rcode.SERVFAIL, rcode.NOTIMP,
                 rcode.REFUSED, rcode.YXDOMAIN, rcode.YXRRSET, rcode.NXRRSET, rcode.NOTAUTH,
                 rcode.NOTZONE, rcode.BADVERS, rcode.BADSIG, rcode.BADKEY, rcode.BADTIME,
                 rcode.BADMODE, rcode.BADNAME, rcode.BADALG, rcode.BADTRUNC,
                 rcode.BADCOOKIE]

CRT_ERR: list = ['UNABLE_TO_GET_ISSUER_CERT', 'UNABLE_TO_GET_CRL', 'UNABLE_TO_DECRYPT_CERT_SIGNATURE',
                 'UNABLE_TO_DECRYPT_CRL_SIGNATURE', 'UNABLE_TO_DECODE_ISSUER_PUBLIC_KEY', 'CERT_SIGNATURE_FAILURE',
                 'CRL_SIGNATURE_FAILURE',
                 'CERT_NOT_YET_VALID', 'CERT_HAS_EXPIRED', 'CRL_NOT_YET_VALID', 'CRL_HAS_EXPIRED',
                 'ERROR_IN_CERT_NOT_BEFORE_FIELD',
                 'ERROR_IN_CERT_NOT_AFTER_FIELD', 'ERROR_IN_CRL_LAST_UPDATE_FIELD', 'ERROR_IN_CRL_NEXT_UPDATE_FIELD',
                 'OUT_OF_MEM',
                 'DEPTH_ZERO_SELF_SIGNED_CERT', 'SELF_SIGNED_CERT_IN_CHAIN', 'UNABLE_TO_GET_ISSUER_CERT_LOCALLY',
                 'CERT_CHAIN_TOO_LONG',
                 'UNABLE_TO_VERIFY_LEAF_SIGNATURE', 'CERT_REVOKED', 'INVALID_CA', 'PATH_LENGTH_EXCEEDED',
                 'INVALID_PURPOSE', 'CERT_UNTRUSTED',
                 'CERT_REJECTED', 'ERR_TLS_CERT_ALTNAME_INVALID']
