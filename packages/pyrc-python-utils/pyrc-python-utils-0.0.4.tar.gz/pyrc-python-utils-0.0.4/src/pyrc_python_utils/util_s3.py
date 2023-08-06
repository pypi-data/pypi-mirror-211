# TODO: Clean up comments
# TODO: Add move and copy functions
# TODO: Add Unit Tests
import os
import re
from typing import Optional, List

import boto3
from boto3.s3.transfer import TransferConfig, S3Transfer
from botocore.client import BaseClient
from botocore.exceptions import BotoCoreError, ClientError

from . import util_file as util_file
from . import util_string as util_string


class S3:
    def __init__(self, region_name, aws_access_key_id, aws_secret_access_key):

        self._region_name = region_name

        try:
            self.s3 = boto3.client(
                's3',
                region_name=region_name,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
            )

        except Exception as e:
            raise Exception(f"Failed to create S3 client: '{e}'") from e

    class S3Bucket:
        def __init__(self, client: BaseClient, name: str):

            try:
                client.head_bucket(Bucket=name)
                self._name = name
                self._client = client
            except ClientError as e:
                error_code = int(e.response['Error']['Code'])
                if error_code == 404:
                    raise ValueError(f"Bucket '{name}' does not exist.")
                else:
                    raise

        @property
        def name(self):
            return self._name

        def is_empty(self) -> bool:
            response = self._client.list_objects_v2(Bucket=self._name)
            # 'KeyCount' is the number of keys in the bucket
            return response['KeyCount'] == 0

        def empty(self):
            while True:
                # Note the 'MaxKeys' parameter
                # This is the maximum number of objects that can be returned in a response.
                # The default value is 1000, so we use that here.
                response = self._client.list_objects_v2(Bucket=self._name, MaxKeys=1000)

                # If there are no objects in the bucket, break the loop.
                if 'Contents' not in response:
                    break

                # Prepare the format of the objects for deletion
                objects = [{'Key': obj['Key']} for obj in response['Contents']]

                # Delete the objects
                self._client.delete_objects(Bucket=self._name, Delete={'Objects': objects})

        def create_folder(self, folder_path: str) -> None:
            """
            Creates a folder in an Amazon S3 bucket if it does not already exist.

            :param folder_path: S3 folder name to create.
            :type folder_path: str
            """
            folder_path = self._prepare_folder_path(folder_path)

            # Create folder if it doesn't already exist
            if not self._object_exists(folder_path):
                self._client.put_object(Bucket=self._name, Key=folder_path)

        def file_count(self,
                       folder_path: Optional[str] = None,
                       file_match_regex: Optional[str] = None,
                       folder_match_regex: Optional[str] = None,
                       recursive: Optional[bool] = False,
                       recursion_depth: Optional[int] = -1) -> int:
            return len(self.get_file_list(folder_path,
                                          file_match_regex,
                                          folder_match_regex,
                                          recursive,
                                          recursion_depth))

        def get_file_list(self,
                          folder_path: Optional[str] = None,
                          file_match_regex: Optional[str] = None,
                          folder_match_regex: Optional[str] = None,
                          recursive: Optional[bool] = False,
                          recursion_depth: Optional[int] = -1) -> List[str]:

            """
            Return a list of files in an S3 bucket within a specific folder that matches a certain regex pattern.

            :param folder_path: The path to the folder in the S3 bucket.
            :type folder_path: str
            :param file_match_regex: Optional regex to filter the files. Default is None, which matches all files.
            :type file_match_regex: Optional[str]
            :param folder_match_regex: Optional regex to filter the folders during recursive search.
                                 Default is None, which matches all folders.
            :type folder_match_regex: Optional[str]
            :param recursive: Whether to recursively traverse sub-folders. Default is False.
            :type recursive: Optional[bool]
            :param recursion_depth: The maximum depth to recurse. -1 means no limit. Default is -1.
            :type recursion_depth: Optional[int]
            :return: A list of matching file paths.
            :rtype: List[str]
            """

            folder_path = self._prepare_folder_path(folder_path)
            files = []

            paginator = self._client.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket=self._name, Prefix=folder_path, Delimiter='/'):
                # Process files in the current folder
                for obj in page.get('Contents', []):
                    file_path = obj['Key']
                    # Ensure the object is not a directory before adding to the list
                    if not file_path.endswith('/'):
                        file_name = os.path.basename(file_path)
                        if file_match_regex is None or re.match(file_match_regex, file_name):
                            files.append(file_path)

                # Process sub-folders
                if recursive and recursion_depth != 0:
                    for subdir in page.get('CommonPrefixes', []):
                        subdir_path = subdir['Prefix']
                        if folder_match_regex is None or re.match(folder_match_regex, subdir_path.strip('/')):
                            files += self.get_file_list(subdir_path, file_match_regex, folder_match_regex, recursive,
                                                        recursion_depth - 1)

            return files

        def upload_file(self,
                        local_file_path: str,
                        folder_path: Optional[str] = None,
                        file_name: Optional[str] = None,
                        overwrite_file: Optional[bool] = True):

            """
            Upload a file to an Amazon S3 bucket.

            :param local_file_path: Path of the local file to upload.
            :type local_file_path: str
            :param folder_path: Folder path in the S3 bucket.
            :type folder_path: Optional[str]
            :param file_name: Name to give to the file in the S3 bucket.
            :type file_name: Optional[str]
            :param overwrite_file: If False, append a counter to the filename if a file with the same name exists.
            :type overwrite_file: Optional[bool]
            :raises ValueError: If the types of bucket_name or local_file are not a string.
            :raises FileNotFoundError: If local_file does not exist.
            :raises Exception: If the upload fails.
            """

            # Check if the local file exists
            if not os.path.isfile(local_file_path):
                raise FileNotFoundError(f"No such file: '{local_file_path}'")

            # If a file_path is provided, ensure the corresponding folder exists in the S3 bucket
            if folder_path:
                self.create_folder(folder_path)

            # If file_name is not provided, use the local file's name
            if file_name is None:
                file_name = os.path.basename(local_file_path)

            # If overwrite_file is False and a file with the same name exists in the S3 bucket,
            # append a counter to the filename
            if not overwrite_file:
                file_name = self._get_next_available_filename(folder_path, file_name)

            # Create the full path of the file in the S3 bucket
            full_path = f"{folder_path}/{file_name}" if folder_path else file_name

            # Upload the file using S3Transfer
            try:
                transfer_config = TransferConfig(multipart_threshold=1024 * 25, max_concurrency=10,
                                                 multipart_chunksize=1024 * 25, use_threads=True)
                transfer = S3Transfer(self._client, config=transfer_config)
                transfer.upload_file(local_file_path, self._name, full_path)
            except Exception as e:
                raise IOError("Upload failed") from e

        def upload_files(self,
                         local_file_list: list[str],
                         folder_path: Optional[str] = None,
                         overwrite_file: Optional[bool] = True):

            for file_path in local_file_list:
                # Upload the file
                self.upload_file(file_path, folder_path, overwrite_file=overwrite_file)

        def download_file(self,
                          file_path: str,
                          local_folder_path: str,
                          local_file_name: Optional[str] = None,
                          overwrite_local_file: Optional[bool] = True) -> None:

            """
            Download a file from a specified bucket to a local directory.

            This function downloads a file from a bucket, saves it to a local directory, and optionally
            renames it. If the local file already exists and overwrite_local_file is set to False, the
            function will create a new file with a unique name to avoid overwriting the existing file.

            Note: Raises an IOError if local_file_path is not a writable directory or does not exist.
            Note: Raises an FileNotFoundError if file_path does not exist.

            :param file_path: The name of the file in the bucket to be downloaded.
            :type file_path: str
            :param local_folder_path: The local directory where the file should be downloaded.
            :type local_folder_path: str
            :param local_file_name: Optional new name for the downloaded file. Default is None,
            which will use the original file name.
            :type local_file_name: Optional[str]
            :param overwrite_local_file: Whether to overwrite the local file if it already exists. Default is True.
            :type overwrite_local_file: Optional[bool]
            :return: None
            """

            # Validate the local file path, raise error if it's not valid
            if not util_file.file_path_is_valid(local_folder_path):
                raise IOError("local_folder_path must be provided and it must be a writable directory.")

            # Check if the file exists
            self._object_exists(file_path, True)

            # Choose the local file name: if local_file is provided, use it; otherwise use the original file name
            local_file_name = local_file_name or os.path.basename(file_path)

            # Join the path and file name to get the full path
            full_path = os.path.join(local_folder_path, local_file_name)

            # If the file already exists, and we're asked NOT to overwrite it, get a new unique file name
            if not overwrite_local_file and os.path.exists(full_path):
                full_path = util_file.get_next_available_filename(full_path)

            # Download the file from the bucket and save it to the full path
            self._client.download_file(self._name, file_path, full_path)

        def download_files(self,
                           bucket_file_list: list[str],
                           local_folder_path: str,
                           overwrite_local_file: Optional[bool] = True):

            for bucket_file in bucket_file_list:
                self.download_file(bucket_file, local_folder_path, overwrite_local_file=overwrite_local_file)

        def delete_file(self, file_path: str):

            try:
                self._client.delete_object(Bucket=self.name, Key=file_path)
            except Exception as e:
                raise IOError(f"Delete failed for file_path: '{file_path}'") from e

        def delete_files(self, bucket_file_list: list[str]):
            for file_path in bucket_file_list:
                # Delete the file
                self.delete_file(file_path)

        def delete_folder(self, folder_path: Optional[str] = None):
            """
            Delete a "folder" and its contents in an S3 bucket.
            :param folder_path: "Folder" to delete
            """
            folder_path = self._prepare_folder_path(folder_path)

            paginator = self._client.get_paginator('list_objects_v2')

            # Delete each object from the "folder"
            for page in paginator.paginate(Bucket=self._name, Prefix=folder_path):
                for obj in page.get('Contents', []):
                    self._client.delete_object(Bucket=self._name, Key=obj['Key'])

            # Delete the "folder" itself - assuming it's not the root
            if not util_string.is_empty(folder_path):
                self._client.delete_object(Bucket=self._name, Key=folder_path)

        def _is_folder(self, object_path: str) -> bool:

            # Check if the file exists
            self._object_exists(object_path, True)

            # Is this a Directory?
            if object_path.endswith("/"):
                return True

            return False

        def _is_file(self, object_path: str) -> bool:
            return not self._is_folder(object_path)

        def _object_exists(self, object_path: str, raise_not_found_exception: Optional[bool] = False) -> bool:

            """
            Checks if an object (file or folder) exists in an Amazon S3 bucket.

            Note: When searching for folders, suffix the folder name with '/'
            e.g.,
                test_folder_1/
                test_folder_1/test_folder_1_1/


            :param object_path: S3 object to check.
            :type object_path: str
            :return: True if the object exists, else False.
            :rtype: bool
            :raises BotoCoreError: For exceptions in the Boto core modules.
            :raises ClientError: For AWS service errors.
            """

            try:
                self._client.head_object(Bucket=self._name, Key=object_path)
            except ClientError as e:
                # If a client error is thrown, then check that it was a 404 error.
                # If it was a 404 error, then the file does not exist.
                if int(e.response['Error']['Code']) == 404:
                    if raise_not_found_exception:
                        raise Exception(f"Object not found at: '{object_path}'") from e
                    else:
                        return False
                else:
                    # Something else has gone wrong.
                    raise Exception(f"Object lookup failed due to ClientError: {e}") from e
            except BotoCoreError as e:
                raise Exception(f"Object lookup failed due to BotoCoreError: {e}") from e

            return True

        @staticmethod
        def _prepare_folder_path(folder_path):
            # If a folder is empty/none, assuming root folder
            if util_string.is_empty(folder_path):
                folder_path = ''
                # Otherwise, ensure folder ends with '/'
            elif not folder_path.endswith('/'):
                folder_path += '/'

            return folder_path

        def _get_next_available_filename(self, file_path: str, file_name: str) -> str:
            """
            Get the next available filename in an Amazon S3 bucket. If a file with the same name exists in the bucket,
            append a counter to the filename.

            :param file_path: Folder path in the S3 bucket.
            :type file_path: str
            :param file_name: Name of the file.
            :type file_name: str
            :return: Next available filename.
            :rtype: str
            """

            # Split the file name into name and extension
            base, ext = os.path.splitext(file_name)

            counter = 1
            while True:
                # Add a counter to the filename if a file with the same name exists
                file = f"{base}_{counter}{ext}" if counter > 1 else file_name
                # Create the full path of the file in the S3 bucket
                full_path = f"{file_path}/{file}" if file_path else file
                # Check if a file with the same name exists in the bucket
                if not self._object_exists(full_path):
                    # If no file with the same name exists, break the loop
                    break
                # If a file with the same name exists, increment the counter and continue the loop
                counter += 1

            # Return the next available filename
            return file

    def get_bucket(self, bucket_name) -> S3Bucket:
        return self.S3Bucket(self.s3, bucket_name)

    def create_bucket(self, bucket_name, return_existing: Optional[bool] = False) -> S3Bucket:
        try:
            if self.bucket_exists(bucket_name) and return_existing == True:
                return self.get_bucket(bucket_name)
            else:
                location = {'LocationConstraint': self._region_name}
                self.s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

                return self.S3Bucket(self.s3, bucket_name)
        except Exception as e:
            raise Exception(f"Error creating bucket {bucket_name}. {e}")

    def delete_bucket(self, bucket_name: str, force_delete: Optional[bool] = False):
        try:
            if force_delete:
                bucket = self.get_bucket(bucket_name)
                bucket.empty()

            self.s3.delete_bucket(Bucket=bucket_name)
        except Exception as e:
            raise Exception(f"Error deleting bucket {bucket_name}. {e}")

    def bucket_exists(self, bucket_name: str):
        try:
            self.s3.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = e.response['Error']['Code']
            if error_code == '404':
                return False
        return True
