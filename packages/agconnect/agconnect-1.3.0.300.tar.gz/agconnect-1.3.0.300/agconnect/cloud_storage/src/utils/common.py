# Copyright (c) Huawei Technologies Co., Ltd. 2023. All rights reserved.

import json
import logging
import math
import random


def is_json_string(value: str) -> bool:
    try:
        json.loads(value)
        return True
    except Exception as e:
        logging.error(e)
        return False


def generate_path(value: str) -> str:
    canonical_path = '/'.join([item for item in value.split('/') if item])
    if value.endswith('/'):
        canonical_path += '/'
    return canonical_path


def random_string(length: int) -> str:
    chars = '0123456789abcdefghijklmnopqrstuvwxyz'
    result = ''
    for i in range(length, 0, -1):
        result += chars[math.floor(random.random() * len(chars))]
    return result
