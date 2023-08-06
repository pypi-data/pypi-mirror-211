# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import json
import os
import time
import logging

from datetime import datetime
from loguru import logger as loguru_logger
from logging.handlers import RotatingFileHandler

from agconnect.common_server.src.error.error import AGCException
from agconnect.common_server.src.error.error_message import ErrorCodeConstant

DEFAULT_LOG_DIR = '../logs'

DEFAULT_LOG_LEVEL = 'INFO'

DEFAULT_MAX_SIZE = '20m'

DEFAULT_MAX_FILES = '14d'

DEFAULT_PREFIX = 'common'

DEFAULT_META_INFO = 'common_server'

DEFAULT_FILE_SWITCH = 'off'

DEFAULT_CONSOLE_SWITCH = 'on'

DEFAULT_LEVEL_COLORS = {
    "TRACE": "cyan",
    "DEBUG": "blue",
    "INFO": "",
    "SUCCESS": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "RED"
}

DEFAULT_DIRECTORY = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../logging_config.json'))

local_time = time.localtime()
now = datetime(local_time[0], local_time[1], local_time[2], local_time[3], local_time[4], local_time[5])
DT_STRING = now.strftime("-%m-%d-%Y-%H")


def log_configuration(config_path: str) -> logging.Logger:
    logging_config = read_config_file(config_path)
    config_info = get_config_info(logging_config)
    log_directory = os.path.normpath(os.path.join(os.path.dirname(
        config_path), config_info[2]))
    try:
        os.mkdir(log_directory)
    except OSError:
        pass

    transports_config = None
    error_file = None
    log_file = None

    if config_info[0] == 'on' and isinstance(config_info[0], str):
        error_file = os.path.normpath(os.path.join(log_directory, 'error.log'))
        log_file = os.path.normpath(os.path.join(
            log_directory, config_info[1] + "{}.log".format(DT_STRING)))

    condition_1 = config_info[0] == 'on' and isinstance(config_info[0], str)
    condition_2 = config_info[8] == 'on' and isinstance(config_info[0], str)
    if condition_1 or condition_2:
        transports_config = log_transports_config(
            config_info, error_file, log_file)

    logger = create_instance(config_info=config_info, transports_config=transports_config)

    return logger


def read_config_file(config_path):
    try:
        with open(config_path, 'r') as file:
            data = json.load(file)
        logging_config = data
    except Exception as error:
        raise AGCException(ErrorCodeConstant.FS_READ_FAIL) from error
    return logging_config


def get_config_info(logging_config):
    file_switch = DEFAULT_FILE_SWITCH
    config_file_switch = logging_config['file_switch']
    if config_file_switch:
        file_switch = config_file_switch

    prefix = DEFAULT_PREFIX
    config_prefix = logging_config['file_name_prefix']
    if config_prefix:
        prefix = config_prefix

    log_dir = DEFAULT_LOG_DIR
    config_log_directory = logging_config['path']
    if config_log_directory:
        log_dir = config_log_directory

    file_log_level = DEFAULT_LOG_LEVEL
    config_file_log_level = logging_config['file_level']
    if config_file_log_level:
        file_log_level = config_file_log_level

    log_max_size = DEFAULT_MAX_SIZE
    config_log_max_size = logging_config['maxSize']
    if config_log_max_size:
        log_max_size = config_log_max_size

    log_max_files = DEFAULT_MAX_FILES
    config_log_max_files = logging_config['maxFiles']
    if config_log_max_files:
        log_max_files = config_log_max_files

    console_log_level = DEFAULT_LOG_LEVEL
    config_console_log_level = logging_config['console_level']
    if config_console_log_level:
        console_log_level = config_console_log_level

    meta_info = DEFAULT_META_INFO
    config_meta_info = logging_config['service']
    if config_meta_info:
        meta_info = config_meta_info

    console_switch = DEFAULT_CONSOLE_SWITCH
    config_console_switch = logging_config['console_switch']
    if config_console_switch:
        console_switch = config_console_switch

    level_colors = DEFAULT_LEVEL_COLORS
    config_level_colors = logging_config['level_colors']
    if config_level_colors:
        level_colors = config_level_colors

    return_list = (file_switch, prefix, log_dir, file_log_level,
                   log_max_size, log_max_files, console_log_level,
                   meta_info, console_switch, level_colors)
    return return_list


def log_transports_config(config_info, error_file: str, log_file: str):
    file = None
    rotate_file = None

    if error_file:
        file = logging.FileHandler(filename=error_file, )
    if log_file:
        rotate_file = RotatingFileHandler(log_file, mode='a', maxBytes=int(config_info[4]),
                                          backupCount=int(config_info[5]), encoding=None, delay=False)

    log_transports = {
        'console_config': logging.StreamHandler(),
        'file': file,
        'rotate_file': rotate_file
    }
    print(log_transports)
    return log_transports


formatter = logging.Formatter(
    fmt='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%m-%d %H:%M:%S')


def create_instance(config_info, transports_config):
    loguru_logger.remove()
    if config_info[0] == 'on' and isinstance(config_info[0], str):
        file_handler = transports_config['file']
        loguru_logger.add(file_handler, level='ERROR')
        rotate_file_handler = transports_config['rotate_file']
        loguru_logger.add(rotate_file_handler, level=config_info[3])

    if config_info[8] == 'on' and isinstance(config_info[8], str):
        console_handler = transports_config['console_config']
        for level, color in config_info[9].items():
            if color:
                loguru_logger.level(level, color=f"<{color}><bold>")
        loguru_logger.add(console_handler, colorize=True, level=config_info[6])

        return loguru_logger
