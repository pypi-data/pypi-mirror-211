# Copyright (c) Huawei Technologies Co., Ltd. 2023. All rights reserved.

import re
from typing import Any

from agconnect.cloud_storage.src.shared.shared_dataclass_stream_file import BucketMetadata
from agconnect.cloud_storage.src.exception.agconnect_cloud_storage_exception import (
    invalid_bucket, invalid_bucket_metadata, invalid_bucket_string, invalid_cors_config,
    invalid_destination_string, invalid_exacting_cors_config,
    invalid_file_string, invalid_area_string,
    invalid_metadata_operation, invalid_null_param)


def validate_bucket_name(func: str, name: str):
    regex = re.compile("^[a-z0-9][a-z0-9-]{1,55}[a-z0-9]$")
    if not name or not regex.match(name):
        raise invalid_bucket(func)


def validate_bucket_name_string(func: str, name: str):
    regex = r"^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$"
    if not name or not re.match(regex, name):
        raise invalid_bucket_string(func)


def validate_area(func: str, area: str):
    areas = ['CN', 'RU', 'SG', 'DE']
    if area not in areas:
        raise invalid_area_string(func)


def validate_destination_string(func: str, des: str):
    if not validate_storage_object(des):
        raise invalid_destination_string(func)


def validate_file_name(func: str, name: str):
    if not validate_storage_object(name):
        raise invalid_file_string(func)


def validate_bucket_metadata(func: str, metadata: BucketMetadata):
    if not metadata or not metadata.cors:
        raise invalid_bucket_metadata(func)


def validate_cors_config(func: str, config):
    if not config:
        raise invalid_cors_config(func, '')

    for cor in config:
        origins = cor.get("origins")
        if not origins:
            raise invalid_exacting_cors_config(func, 'origins')

        for origin in origins:
            if len(origin or '') > 1024:
                raise invalid_exacting_cors_config(func, 'Origin is too long than 1024')
            if len(origin or '') == 0:
                raise invalid_exacting_cors_config(func, 'Origin should not be empty.')

        headers = cor.get("headers")
        if headers:
            for header in headers:
                if len(header or '') > 1024:
                    raise invalid_exacting_cors_config(func, 'Header is too long than 1024.')
                if len(header or '') == 0:
                    raise invalid_exacting_cors_config(func, 'Header should not be empty.')

        expose_headers = cor.get("exposeHeaders")
        if expose_headers:
            for expose_header in expose_headers:
                if len(expose_header or '') > 1024:
                    raise invalid_exacting_cors_config(func, 'ExposeHeader is too long than 1024.')
                if len(expose_header or '') == 0:
                    raise invalid_exacting_cors_config(func, 'ExposeHeader should not be empty.')

        max_age_seconds = cor.get("maxAgeSeconds")
        if max_age_seconds and (max_age_seconds < 0 or max_age_seconds >= 10000000):
            raise invalid_exacting_cors_config(func, 'maxAgeSeconds: only a number ranging from 0 to '
                                                     '9999999 is allowed.')


def validate_meta_data_opt(name: str, file_name: str):
    if file_name.endswith('/'):
        raise invalid_metadata_operation()


def validate_not_null(param: Any, name: str):
    if param is None:
        raise invalid_null_param(name)


def validate_storage_object(name: str) -> bool:
    str_value = '#*:?\'"<>|[]'
    for item in name:
        if item in str_value:
            return False
    return True
