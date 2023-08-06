# Copyright (c) Huawei Technologies Co., Ltd. 2023. All rights reserved.

import os
from typing import Optional

from agconnect.cloud_storage.src.impl import storage_management
from agconnect.common_server.src.agc_client import AGCClient
from agconnect.common_server import ServiceFactory


class AGCCloudStorage:
    @staticmethod
    def get_instance(name: Optional[str] = None) -> storage_management.StorageManagement:
        def factory():
            return storage_management.StorageManagement()

        config_path = os.path.normpath(os.path.join(os.path.dirname(__file__), './../../agconnect_cloudstorage.json'))
        storage = ServiceFactory.initialize_service(AGCClient.get_instance(name), "CloudStorage",
                                                    factory, str(config_path))
        return storage
