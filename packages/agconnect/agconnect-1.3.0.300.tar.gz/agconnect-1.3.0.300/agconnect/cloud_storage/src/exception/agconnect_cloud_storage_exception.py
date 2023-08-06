# Copyright (c) Huawei Technologies Co., Ltd. 2023. All rights reserved.

from typing import Optional

from agconnect.cloud_storage import CloudStorageErrorCode
from agconnect.common_server import AGCException
from agconnect.common_server.src.log_config import logger


class AGCCloudStorageException(AGCException):
    def __init__(self, error_code: str, error_message=''):
        my_error_code = {"code": error_code,
                         "message": error_message}
        super().__init__(my_error_code, "AGCCloudStorageError")


def invalid_bucket(func: str) -> AGCCloudStorageException:
    message = f"{func} 'Invalid bucket name. Enter 3 to 57 characters, limited to lowercase letters, digits, " \
              f"and hyphens (-), and starting and ending with a digit or letter."
    return AGCCloudStorageException(error_code=CloudStorageErrorCode.INVALID_BUCKET_STRING, error_message=message)


def invalid_bucket_string(func: str) -> AGCCloudStorageException:
    message = "{}Invalid bucket name. Enter 3 to 63 characters, limited to lowercase letters, " \
              "digits, and hyphens (-), " \
              "and starting and ending with a digit or letter.".format(func)
    return AGCCloudStorageException(error_code=CloudStorageErrorCode.INVALID_BUCKET_STRING, error_message=message)


def invalid_area_string(func: str) -> AGCCloudStorageException:
    message = "{}Invalid area. Area must be one of CN, DE, RU, SG.".format(func)
    return AGCCloudStorageException(error_code=CloudStorageErrorCode.INVALID_AREA_STRING, error_message=message)


def invalid_destination(func: Optional[str] = None) -> AGCCloudStorageException:
    message = "{}Invalid destination. Destination must be string | Bucket | File.".format(func or "")
    return AGCCloudStorageException(error_code=CloudStorageErrorCode.INVALID_DESTINATION, error_message=message)


def invalid_destination_string(func: str) -> AGCCloudStorageException:
    message = "{}Invalid destination. The following special characters are not permitted: " \
              "# * : ? \\ ' \" < > | [ ] .".format(func)
    return AGCCloudStorageException(error_code=CloudStorageErrorCode.INVALID_DESTINATION_STRING, error_message=message)


def parse_destination_string_error() -> AGCCloudStorageException:
    message = "Parse destination failed. The characters must meet the format requirements: {desBucket}/{desName}"
    return AGCCloudStorageException(error_code=CloudStorageErrorCode.DESTINATION_PARSE_ERR, error_message=message)


def invalid_file_string(func: str) -> AGCCloudStorageException:
    message = "{}Invalid file name. The following special characters are not permitted: " \
              "# * : ? \\ ' \" < > | [ ] .".format(func)
    return AGCCloudStorageException(error_code=CloudStorageErrorCode.INVALID_FILE_STRING, error_message=message)


def invalid_bucket_metadata(func: str) -> AGCCloudStorageException:
    message = "{}Invalid bucket metadata. Param cors cannot be null.".format(func)
    return AGCCloudStorageException(error_code=CloudStorageErrorCode.INVALID_BUCKET_METADATA, error_message=message)


def invalid_cors_config(func: str, msg: str) -> AGCCloudStorageException:
    if msg:
        result = " \"{}\" ".format(msg)
    else:
        result = " "
    message = "{}Invalid cors config. Cors config{}cannot be null.".format(func, result)
    return AGCCloudStorageException(error_code=CloudStorageErrorCode.INVALID_CORS_CONFIG, error_message=message)


def invalid_exacting_cors_config(func: str, msg: str) -> AGCCloudStorageException:
    return AGCCloudStorageException(error_code=CloudStorageErrorCode.INVALID_CORS_CONFIG, error_message=msg)


def invalid_null_param(param: str) -> AGCCloudStorageException:
    message = f'Param "{param}" should not be null or undefined.'
    return AGCCloudStorageException(error_code=CloudStorageErrorCode.NULL_PARAM_ERR, error_message=message)


def invalid_credential() -> AGCCloudStorageException:
    message = 'Get configuration from credential failed. Please check your credential file again.'
    return AGCCloudStorageException(error_code=CloudStorageErrorCode.INVALID_CREDENTIAL, error_message=message)


def file_delete_error() -> AGCCloudStorageException:
    message = 'Delete file failed. Please try again.'
    return AGCCloudStorageException(error_code=CloudStorageErrorCode.FILE_DELETE_ERR, error_message=message)


def generate_token_error() -> AGCCloudStorageException:
    message = 'Generate token failed. Please check your credential file and try again.'
    return AGCCloudStorageException(error_code=CloudStorageErrorCode.GENERATE_TOKEN_ERR, error_message=message)


def simple_upload_err() -> AGCCloudStorageException:
    message = 'The maximum size of a file to be uploaded each time cannot exceed 5 GB.'
    return AGCCloudStorageException(error_code=CloudStorageErrorCode.SIMPLE_UPLOAD_LIMIT_ERR, error_message=message)


def upload_err() -> AGCCloudStorageException:
    message = 'The maximum size of a file to be uploaded cannot exceed 50 GB.'
    return AGCCloudStorageException(error_code=CloudStorageErrorCode.UPLOAD_LIMIT_ERR, error_message=message)


def no_address_available() -> AGCCloudStorageException:
    message = 'No address available now. Please wait or contact the AGC Operator.'
    return AGCCloudStorageException(error_code=CloudStorageErrorCode.NO_ADDRESS_AVAILABLE, error_message=message)


def invalid_metadata_operation() -> AGCCloudStorageException:
    message = 'Can not set metadata for folder.'
    return AGCCloudStorageException(error_code=CloudStorageErrorCode.INVALID_METADATA_OPERATION, error_message=message)


def invalid_path() -> AGCCloudStorageException:
    return AGCCloudStorageException(CloudStorageErrorCode.INVALID_PATH, 'Path should not be directory.')


def bucket_not_found() -> AGCCloudStorageException:
    return AGCCloudStorageException(CloudStorageErrorCode.BUCKET_NOT_FOUND,
                                    'Bucket not found. Please check your bucketName again.')


def sha_not_match() -> AGCCloudStorageException:
    return AGCCloudStorageException(CloudStorageErrorCode.SHA256_NOT_MATCH,
                                    'Failed to verify the object hash. Please check sha256 again or try again.')


def auth_failed() -> AGCCloudStorageException:
    return AGCCloudStorageException(CloudStorageErrorCode.AUTH_FAILED,
                                    'Identity authentication failed. Please check your credential file and try again.')


def no_permission() -> AGCCloudStorageException:
    return AGCCloudStorageException(CloudStorageErrorCode.NO_PERMISSION,
                                    'You don\'t have permission to access the file or directory')


def object_not_found() -> AGCCloudStorageException:
    return AGCCloudStorageException(CloudStorageErrorCode.OBJECT_NOT_FOUND,
                                    'The object doesn\'t exist.')


def quota_exceeded() -> AGCCloudStorageException:
    raise AGCCloudStorageException(CloudStorageErrorCode.QUOTA_EXCEEDED,
                                   'The quota of the bucket has been used up. Please check the payment plan.')


def convert_error_code(status_code: int, ret_code: int, data: str):
    ret_code = int(ret_code)
    if status_code == 500 or status_code == 400:
        if ret_code == 135003 or data == 'Bucket not exist':
            return bucket_not_found()
        elif ret_code == 131009:
            return sha_not_match()
        else:
            logger.error(f'Bad Server Response. Return Code {ret_code}. Status Code {status_code}')
            return AGCCloudStorageException(error_code=CloudStorageErrorCode.BAD_SERVER_RESPONSE,
                                            error_message='Bad server response. Please try again.')
    elif status_code == 401:
        return auth_failed()
    elif status_code == 403:
        return no_permission()
    elif status_code == 404:
        if ret_code == 135003:
            return bucket_not_found()
        else:
            return object_not_found()
    elif status_code == 409:
        return sha_not_match()
    elif status_code == 507:
        return quota_exceeded()
    else:
        return AGCCloudStorageException(error_code=CloudStorageErrorCode.UNKNOWN_ERROR,
                                        error_message='Unknown error occurred.')
