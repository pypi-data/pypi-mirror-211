# Copyright (c) Huawei Technologies Co., Ltd. 2023. All rights reserved.

import asyncio
import hashlib
import os
import urllib.parse
from typing import Any, Optional, List, cast, Union, Dict

from agconnect.cloud_storage.src.model.callback import CreateBucketResponse, \
    BucketExistResponse, GetBucketsResponse, Metadata
from agconnect.cloud_storage.src.shared.shared_dataclass_stream_file import GetCorsResponse, BucketMetadata, Cors
from agconnect.cloud_storage.src.model.options import DeleteFileOptions, GetFilesOptions
from agconnect.cloud_storage.src.utils.validator import validate_bucket_name_string, validate_not_null, validate_area, \
    validate_bucket_metadata, validate_bucket_name, validate_cors_config, validate_file_name
from agconnect.cloud_storage.src.impl.file import File, GetFilesResponse, UploadOptions
from agconnect.cloud_storage.src.request.request import HttpMethod
from agconnect.cloud_storage.src.shared.request_with_storage_shared import generate_res, request
from agconnect.cloud_storage.src.impl.constant import DEFAULT_MAX_KEYS, RESUMABLE_UPLOAD_SIZE, UPLOAD_MAX_SIZE
from agconnect.cloud_storage.src.exception.agconnect_cloud_storage_exception import file_delete_error, invalid_path, \
    upload_err, AGCCloudStorageException
from agconnect.cloud_storage.src.config.config import Config
from agconnect.cloud_storage.src.upload.resumable_upload import OffsetOpt, ResumableUpload, \
    ResumableUploadOpt, get_offset
from agconnect.cloud_storage.src.utils.common import random_string
from agconnect.common_server.src.log_config import logger


class Bucket:
    name: str
    area: str

    def __init__(self, storage, name: str, area: Optional[str] = None):
        validate_not_null(storage, 'StorageManagement')
        validate_bucket_name_string('bucket.constructor: ', name)
        area = area if area else Config.get_instance(storage.name).default_region
        validate_area('bucket.constructor: ', area)
        self.name = name
        self.area = area
        self.storage = storage

    async def create(self, metadata=None) -> CreateBucketResponse:
        validate_bucket_name('bucket.create: ', self.name)
        url = '/v0/'
        headers = {
            'X-Agc-Bucket-Name': self.name + '-' + random_string(5)
        }
        data = None
        if metadata and metadata.get('cors'):
            data = {
                'rules': metadata.get('cors')
            }
        return await generate_res(request(method_type=HttpMethod.PUT, request_uri=url, data=data, request_params=None,
                                          request_headers=headers, storage=self.storage, area=self.area))

    async def delete(self):
        url = '/v0/'
        headers = {
            'X-Agc-Bucket-Name': urllib.parse.quote(self.name)
        }
        return await generate_res(request(method_type=HttpMethod.DELETE, request_uri=url, data=None,
                                          request_params=None, request_headers=headers, storage=self.storage,
                                          area=self.area))

    async def delete_files(self, options: DeleteFileOptions = None):
        truncated: bool = True
        err_result: Any = []
        options = DeleteFileOptions(delimiter=None, max_keys=None, marker=None, prefix=None, force_pause=None) \
            if options is None else options

        async def delete_file(file: File):
            try:
                return await file.delete()
            except Exception as e:
                if options.force_pause:
                    raise file_delete_error() from e
                else:
                    raise e

        while truncated:
            try:
                res: GetFilesResponse = await self.get_files(options)
                if not res.fileList:
                    logger.error('There is no file or directory to delete, please check your bucket and/or options.')
                    raise file_delete_error()
                options.marker = res.marker
                truncated = bool(res.marker)
                limit = asyncio.Semaphore(10)
                async with limit:
                    result = await asyncio.gather(*[delete_file(file) for file in res.fileList])
            except (AGCCloudStorageException, Exception) as e:
                err_result.append(e)
                truncated = False

        if not err_result or len(err_result) == 0:
            return result
        else:
            return err_result

    async def exists(self) -> BucketExistResponse:
        try:
            res: GetBucketsResponse = await self.storage.get_buckets(self.area)
            if res and res.buckets:
                filtered_buckets = list(filter(lambda item: item.bucket_name == self.name, res.buckets))
                if len(filtered_buckets) > 0:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            raise e

    def file(self, name: str) -> File:
        validate_file_name('bucket.file: ', name)
        return File(self, name)

    async def get_files(self, options: GetFilesOptions = None) -> GetFilesResponse:
        url = '/v0/' + self.name
        headers = {}
        data = {}
        if options:
            if options.max_keys:
                data.update({
                    'max-keys': min(options.max_keys, DEFAULT_MAX_KEYS)
                })
            if options.marker:
                data.update({
                    'marker': options.marker
                })
            if options.prefix:
                data.update({
                    'prefix': options.prefix
                })
            if options.delimiter:
                data.update({
                    'delimiter': options.delimiter
                })
        try:
            async with await request(method_type=HttpMethod.GET, request_uri=url, data=None,
                                                request_params=data,
                                                request_headers=headers, storage=self.storage, area=self.area) as res:
                if not res:
                    return GetFilesResponse(dirList=[],
                                            fileList=[])
                resource = await res.json(content_type='text/plain')
                list_result = GetFilesResponse(dirList=[],
                                               fileList=[],
                                               marker=resource.get(MARKER_KEY))
            if resource.get(Contents_KEY):
                for item in resource.get(Contents_KEY):
                    if options.delimiter and item.get('key').endswith(options.delimiter):
                        list_result.dirList.append(item.get('key'))
                    else:
                        file = self.file(item.get('key'))
                        list_result.fileList.append(file)
            if resource.get(PREFIXES_KEY):
                for item in resource.get(PREFIXES_KEY):
                    list_result.dirList.append(item.get('prefix'))
            return list_result
        except Exception as e:
            raise e

    async def set_cors_configuration(self, config: List[Cors]):
        validate_cors_config('bucket.set_cors_configuration: ', config)
        url = '/v0/' + self.name + '?cors'
        headers = {}
        data = {'rules': config}
        return await generate_res(request(method_type=HttpMethod.PUT, request_uri=url, data=data, request_params=None,
                                          request_headers=headers, storage=self.storage, area=self.area))

    async def get_cors_configuration(self) -> GetCorsResponse:
        url = '/v1/' + self.name + '?cors'
        headers = {}
        return await generate_res(request(method_type=HttpMethod.GET, request_uri=url, data=None, request_params=None,
                                          request_headers=headers, storage=self.storage, area=self.area))

    async def set_meta_data(self, metadata: BucketMetadata):
        validate_bucket_metadata('bucket.set_meta_data: ', metadata)
        return await self.set_cors_configuration(cast(List[Cors], metadata.cors))

    async def upload(self, path_str: str, options: UploadOptions = None) -> \
            Union[File, Optional[Metadata]]:
        def progress_callback_function(progress: Dict[str, int] = None):
            logger.info(f"Uploaded: {progress.get('writtenBytes')}/{progress.get('totalBytes')}")
        if options is not None and options.on_upload_progress:
            options = UploadOptions(destination=os.path.basename(path_str),
                                    on_upload_progress=options.on_upload_progress,
                                    sha256=None)
        else:
            options = UploadOptions(destination=os.path.basename(path_str),
                                    on_upload_progress=progress_callback_function,
                                    sha256=None)

        async def upload_file(bucket: Bucket, sha256: str, size: int):
            try:
                async def resumable_upload(offset: int, upload_size: int):
                    try:
                        resumable_upload_opt: ResumableUploadOpt = \
                            ResumableUploadOpt(
                                bucket=bucket,
                                file=file,
                                size=size,
                                storage=bucket.storage,
                                area=bucket.area,
                                offset=offset,
                                upload_size=upload_size,
                                sha256=sha256,
                                on_upload_progress=options.on_upload_progress if isinstance(
                                    options, UploadOptions) and options.on_upload_progress else None)
                        resumable_upload: ResumableUpload = \
                            ResumableUpload(resumable_upload_opt)
                        resp = await resumable_upload.upload(path_str, options.on_upload_progress)
                        return resp
                    except (AGCCloudStorageException, Exception) as e:
                        raise e

                file: File
                if options is not None and isinstance(options.destination, File):
                    file = options.destination
                elif options is not None and options.destination is not None and isinstance(options.destination, str):
                    file_name = os.path.basename(options.destination)
                    validate_file_name('bucket.file: ', file_name)
                    file = bucket.file(file_name)
                else:
                    file_name = os.path.basename(path_str)
                    validate_file_name('bucket.file: ', file_name)
                    file = bucket.file(file_name)
                offset_opt = OffsetOpt(size=size, sha256=sha256, bucket=bucket, file=file)
                try:
                    offset_res = await get_offset(offset_opt, bucket)
                except (AGCCloudStorageException, Exception) as e:
                    raise e
                if offset_res is not None and offset_res.get("uploadStatus") == 'resumable':
                    offset = offset_res.get("receiveBytes")
                elif offset_res is not None and offset_res.get("uploadStatus") == 'finalize':
                    return_value = [file, None]
                    return return_value
                else:
                    offset = 0
                finish = False
                error_value = None
                return_value = None
                while not finish and offset <= os_stat.st_size:
                    try:
                        res = await resumable_upload(offset, min(os_stat.st_size - offset, RESUMABLE_UPLOAD_SIZE))
                        if not res:
                            error_value = 'Upload failed'
                            break
                        if res.get("uploadStatus") == 'resumable':
                            if offset == res.get("receiveBytes"):
                                error_value = res
                                break
                            offset = res.get("receiveBytes")
                        elif res.get("uploadStatus") == 'finalize':
                            offset = os_stat.st_size
                            finish = True
                            return_value = res
                        else:
                            error_value = res
                            break
                    except (AGCCloudStorageException, Exception) as e:
                        error_value = e
                        break
                if error_value:
                    raise error_value
                else:
                    return return_value
            except (AGCCloudStorageException, Exception) as err:
                raise err
        os_stat = os.stat(path_str)
        if os.path.isdir(path_str):
            raise invalid_path()
        if os_stat.st_size > UPLOAD_MAX_SIZE:
            raise upload_err()

        async def read_stream(path: str, update_sha256):
            with open(path, "rb") as f:
                while True:
                    data = f.read(65536)
                    if not data:
                        break
                    update_sha256(data)

        async def calculate_sha256(path: str) -> str:
            sha256_sum = hashlib.sha256()

            def update_sha256(data):
                sha256_sum.update(data)

            await read_stream(path, update_sha256)
            return sha256_sum.hexdigest()

        if options is None or options.sha256 is None:
            sha = await calculate_sha256(path_str)
        else:
            sha = options.sha256

        try:
            res = await upload_file(self, sha, os_stat.st_size)
            return res
        except (AGCCloudStorageException, Exception) as e:
            raise e


MARKER_KEY = 'nextMarker'
PREFIXES_KEY = 'commonPrefixes'
Contents_KEY = 'contents'
