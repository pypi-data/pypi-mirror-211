# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from enum import Enum


class ConditionType(str, Enum):
    BEGINS_WITH = 'BeginsWith'
    ENDS_WITH = 'EndsWith'
    CONTAINS = 'Contains'
    EQUAL_TO = 'EqualTo'
    NOT_EQUAL_TO = 'NotEqualTo'
    GREATER_THAN = 'GreaterThan'
    GREATER_THAN_OR_EQUAL_TO = 'GreaterThanOrEqualTo'
    LESS_THAN = 'LessThan'
    LESS_THAN_OR_EQUAL_TO = 'LessThanOrEqualTo'
    IN = 'In'
    IS_NULL = 'IsNull'
    IS_NOT_NULL = 'IsNotNull'
    ORDER_BY = 'OrderBy'
    LIMIT = 'Limit'
    ASCEND = 'asc'
    DESCEND = 'desc'
    START_AT = 'StartAt'
    START_AFTER = 'StartAfter'
    END_AT = 'EndAt'
    END_BEFORE = 'EndBefore'
    UID = 'Uid'
