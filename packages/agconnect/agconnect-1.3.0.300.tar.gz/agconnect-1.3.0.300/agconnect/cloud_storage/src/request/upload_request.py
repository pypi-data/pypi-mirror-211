# Copyright (c) Huawei Technologies Co., Ltd. 2023. All rights reserved.

from io import BytesIO
from typing import Union
from agconnect.common_server import logger


class EventIOptions:
    def __init__(self, end: bool = False, auto_destroy: bool = False):
        self.end = end
        self.auto_destroy = auto_destroy


class EventIO(BytesIO):

    def __init__(self, writable: Union[BytesIO, bool, None] = None,
                 readable: Union[BytesIO, bool, None] = None,
                 options: EventIOptions = None, max_listeners: int = 10, on_progress=None):
        super().__init__()
        self.on_progress = on_progress
        self.max_listeners = max_listeners
        self.writable = writable
        self.readable = readable or self
        self.destroyed = False
        self.options = options
        if options and isinstance(options, EventIOptions):
            self.auto_destroy = options.auto_destroy
            self.end = options.end
        else:
            self.auto_destroy = False
            self.end = False

    def read(self, *args, **kwargs):
        result = super().read(*args, **kwargs)
        return result

    def write(self, *args, **kwargs):
        result = super().write(*args, **kwargs)
        return result

    def close(self, error: str = None):
        self.destroyed = True
        readable_is_closeable = self.readable and hasattr(self.readable, 'close')
        readable_is_not_eventio = not isinstance(self.readable, EventIO)
        not_destroyed = not self.destroyed
        if readable_is_closeable and readable_is_not_eventio and not_destroyed:
            self.readable.close()
        if self.writable:
            is_writable_closeable = hasattr(self.writable, 'close')
            is_not_eventio = not isinstance(self.writable, EventIO)
            is_not_destroyed = not self.destroyed
            if is_writable_closeable and is_not_eventio and is_not_destroyed:
                self.writable.close()

        if error is not None:
            logger.error(f"Error occurred during stream operation: {error}")

    def set_writable(self, writable):
        self.writable = writable

    def set_readable(self, readable):
        self.readable = readable

    def __del__(self):
        if self.options is not None and self.options.auto_destroy:
            self.close()
