# Copyright (c) Huawei Technologies Co., Ltd. 2023. All rights reserved.

import asyncio
import threading
from typing import Callable
import os


class FileReader(object):
    def __init__(self, file_obj, file_path, on_progress: Callable):
        os_stat = os.stat(file_path)
        self.total_size = os_stat.st_size
        self.amount_seen = 0
        self.file_obj = file_obj
        self.on_progress = on_progress

    async def generate_chunks(self):
        while True:
            chunk = self.file_obj.read(4 * 1024 * 1024)
            if not chunk:
                return
            self.amount_seen += len(chunk)
            if self.on_progress:
                if asyncio.iscoroutinefunction(self.on_progress):
                    progress = {'writtenBytes': self.amount_seen, 'totalBytes': self.total_size}
                    asyncio.create_task(self.on_progress(progress))
                else:
                    progress = {'writtenBytes': self.amount_seen, 'totalBytes': self.total_size}
                    thread = threading.Thread(target=self.on_progress, args=(progress,), daemon=True)
                    thread.start()
            yield chunk
