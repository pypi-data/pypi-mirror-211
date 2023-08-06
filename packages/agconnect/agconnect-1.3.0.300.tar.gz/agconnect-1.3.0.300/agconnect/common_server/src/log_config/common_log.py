# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import json
import os

from agconnect.common_server.src.log_config.logging_config import log_configuration

directory = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../logging_config.json'))
logger = log_configuration(directory)


def update_level_color(trace_color: str = None, debug_color: str = None, info_color: str = None,
                       success_color: str = None, warning_color: str = None, error_color: str = None,
                       critical_color: str = None):
    with open(directory, 'r') as file:
        data = json.load(file)
    if trace_color or trace_color == '':
        data['level_colors']['TRACE'] = trace_color
    if debug_color or debug_color == '':
        data['level_colors']['DEBUG'] = debug_color
    if info_color or info_color == '':
        data['level_colors']['INFO'] = info_color
    if success_color or success_color == '':
        data['level_colors']['SUCCESS'] = success_color
    if warning_color or warning_color == '':
        data['level_colors']['WARNING'] = warning_color
    if error_color or error_color == '':
        data['level_colors']['ERROR'] = error_color
    if critical_color or critical_color == '':
        data['level_colors']['CRITICAL'] = critical_color
    fd = os.open(directory, os.O_CREAT | os.O_WRONLY, 0o644)
    with os.fdopen(fd, 'w') as file:
        file.truncate()
        json.dump(data, file, indent=4)
    updated_logger = log_configuration(directory)
    return updated_logger


def update_config(logger_level=None, file_switch=None, console_switch=None, log_file_path=None, file_level=None,
                  console_level=None):
    with open(directory, 'r') as file:
        data = json.load(file)
    if logger_level:
        data['logger_level'] = logger_level
    if file_switch:
        data['file_switch'] = file_switch
    if console_switch:
        data['console_switch'] = console_switch
    if log_file_path:
        data['path'] = log_file_path
    if file_level:
        data['file_level'] = file_level
    if console_level:
        data['console_level'] = console_level
    fd = os.open(directory, os.O_CREAT | os.O_WRONLY, 0o644)
    with os.fdopen(fd, 'w') as file:
        file.truncate()
        json.dump(data, file, indent=4)
    updated_logger = log_configuration(directory)
    return updated_logger
