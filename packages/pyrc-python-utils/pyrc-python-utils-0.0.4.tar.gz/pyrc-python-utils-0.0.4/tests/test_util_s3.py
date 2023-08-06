import os
import uuid

import pytest
from dotenv import load_dotenv

from src.pyrc_python_utils import util_file
from src.pyrc_python_utils.util_s3 import S3

TEST_FILE_NAME = "test_file.txt"


@pytest.fixture(scope='module', autouse=True)
def setup_and_teardown_module():
    """ Setup and Teardown of testing bucket"""

    # S3 Sandbox credentials
    load_dotenv()
    aws_access_key_id = os.getenv('S3_AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('S3_AWS_SECRET_ACCESS_KEY')
    aws_region_name = os.getenv('S3_AWS_REGION_NAME')

    s3 = S3(aws_region_name, aws_access_key_id, aws_secret_access_key)

    # Establish a unique test bucket
    unique_id = uuid.uuid5(uuid.NAMESPACE_DNS, str(uuid.getnode()))
    bucket_name = 'python-utils-test-' + str(unique_id)

    bucket = s3.create_bucket(bucket_name, True)

    yield bucket

    # Teardown: Code here will run once after all tests in the module have completed.
    s3.delete_bucket(bucket_name, True)


@pytest.fixture(scope='function', autouse=True)
def setup_and_teardown_function(setup_and_teardown_module):
    """ Empty bucket after each test """
    bucket = setup_and_teardown_module
    bucket.empty()


@pytest.fixture
def test_file_path():
    # Test file used throughout testing
    local_file = TEST_FILE_NAME
    return os.path.join(os.path.dirname(__file__), local_file)


@pytest.fixture
def test_file_list_local():
    # List of files in the local folder - used for upload testing
    return util_file.get_file_list(os.path.dirname(__file__))


def test_upload_file(setup_and_teardown_module, test_file_path):
    """ Upload test file into root folder of bucket """
    bucket = setup_and_teardown_module

    bucket.upload_file(test_file_path)
    assert bucket._object_exists(TEST_FILE_NAME)


def test_upload_file_rename(setup_and_teardown_module, test_file_path):
    """ Upload and rename test file into the root folder of bucket """

    bucket = setup_and_teardown_module

    bucket.upload_file(test_file_path, file_name='test_file_rename.txt')
    assert bucket._object_exists("test_file_rename.txt")


def test_upload_file_folder(setup_and_teardown_module, test_file_path):
    """ Upload test file into sub-folder folder of bucket """

    bucket = setup_and_teardown_module

    bucket.upload_file(test_file_path, "test_folder_1")
    assert bucket._object_exists("test_folder_1/" + TEST_FILE_NAME)

    # Rename uploaded file
    bucket.upload_file(test_file_path, "test_folder_1", file_name="test_file_2.txt")
    assert bucket._object_exists("test_folder_1/test_file_2.txt")


def test_upload_file_overwrite(setup_and_teardown_module, test_file_path):
    """
    Upload test file into various folders and rename with counter suffix if the file already exists

    test_file.txt -> test_file_2.txt

    """
    bucket = setup_and_teardown_module

    bucket.upload_file(test_file_path)
    bucket.upload_file(test_file_path, overwrite_file=False)
    assert bucket._object_exists("test_file_2.txt")

    bucket.upload_file(test_file_path, file_name="test_file_2.txt", overwrite_file=False)
    assert bucket._object_exists("test_file_2_2.txt")

    bucket.upload_file(test_file_path, "test_folder_1")
    bucket.upload_file(test_file_path, "test_folder_1", overwrite_file=False)
    assert bucket._object_exists("test_folder_1/test_file_2.txt")


def test_upload_files(setup_and_teardown_module, test_file_list_local):
    """ Upload files from local folder into bucket root"""
    bucket = setup_and_teardown_module

    bucket.upload_files(test_file_list_local)
    assert bucket._object_exists(os.path.basename(__file__))
    assert len(test_file_list_local) == bucket.file_count()


def test_upload_files_folder(setup_and_teardown_module, test_file_list_local):
    """ Upload files from local folder into bucket sub-folder """
    bucket = setup_and_teardown_module

    bucket.upload_files(test_file_list_local, "test_folder_1")
    assert bucket._object_exists("test_folder_1/" + os.path.basename(__file__))
    assert len(test_file_list_local) == bucket.file_count("test_folder_1")


def test_upload_files_overwrite(setup_and_teardown_module, test_file_list_local):
    """
    Upload files from local folder into bucket root folder, and rename with counter suffix if the file already exists

    test_file.txt -> test_file_2.txt

    """
    bucket = setup_and_teardown_module

    bucket.upload_files(test_file_list_local)
    bucket.upload_files(test_file_list_local, overwrite_file=False)

    file_name, file_extension = os.path.splitext(os.path.basename(__file__))
    assert bucket._object_exists(file_name + "_2" + file_extension)

    # Since we uploaded the same files twice, the count of files should have doubled as a result of the rename
    assert len(test_file_list_local) * 2 == bucket.file_count()


def test_get_file_list(setup_and_teardown_module, test_file_list_local):
    """ Get all files from the bucket root folder """
    bucket = setup_and_teardown_module

    bucket.upload_files(test_file_list_local)
    bucket.upload_files(test_file_list_local, "test_folder_1")

    # Even though we uploaded the test files twice, get_file_list() defaults to non-recursive, so the only files
    # should be from the root, and not from the sub-folder
    file_count = bucket.file_count()
    assert len(bucket.get_file_list()) == file_count


def test_get_file_list_folder(setup_and_teardown_module, test_file_list_local):
    """ Get all files from the bucket sub-folder """
    bucket = setup_and_teardown_module

    bucket.upload_files(test_file_list_local, "test_folder_1")

    file_count = bucket.file_count("test_folder_1")
    assert len(bucket.get_file_list(folder_path="test_folder_1")) == file_count


def test_get_file_list_regex(setup_and_teardown_module, test_file_list_local):
    """ Get all files from the bucket root that folder that match the regex """
    bucket = setup_and_teardown_module

    bucket.upload_files(test_file_list_local)
    file_list = bucket.get_file_list(file_match_regex=TEST_FILE_NAME)
    assert len(file_list) == 1


def test_get_file_list_recursive(setup_and_teardown_module, test_file_list_local):
    """ Get all files (recursively) matching the regex parameters """
    bucket = setup_and_teardown_module

    upload_multi_files_folders(bucket, test_file_list_local)

    # Get all files (recursively) matching the file regex
    file_list = bucket.get_file_list(file_match_regex=TEST_FILE_NAME, recursive=True)
    assert len(file_list) == 3

    # Get all files (recursively) matching the file and folder regex
    file_list = bucket.get_file_list(file_match_regex=TEST_FILE_NAME, folder_match_regex="test_folder_1$",
                                     recursive=True)
    assert len(file_list) == 1


def test_get_file_list_recursion_depth(setup_and_teardown_module, test_file_list_local):
    """ Get all files (recursively) for a particular depth and matching a file regex """

    bucket = setup_and_teardown_module

    upload_multi_files_folders(bucket, test_file_list_local)

    # The test file was added 3 times, but only the folders at a depth of 1 are eligible
    file_list = bucket.get_file_list(file_match_regex=TEST_FILE_NAME, recursive=True, recursion_depth=1)
    assert 2 == len(file_list)


def test_download_file(setup_and_teardown_module, test_file_path, tmp_path):
    """ Download test files """
    bucket = setup_and_teardown_module
    download_folder = str(tmp_path)

    bucket.upload_file(test_file_path)

    # Upload to sub-folder and rename
    bucket.upload_file(test_file_path, "test_folder_1", file_name="test_file_2.txt")

    # Download files
    bucket.download_file(os.path.basename(test_file_path), download_folder)
    bucket.download_file("test_folder_1/test_file_2.txt", download_folder)

    file_path = os.path.join(download_folder, os.path.basename(test_file_path))
    assert os.path.isfile(file_path)

    file_path = os.path.join(download_folder, "test_file_2.txt")
    assert os.path.isfile(file_path)


def test_download_file_rename(setup_and_teardown_module, test_file_path, tmp_path):
    """ Download test file and rename """

    bucket = setup_and_teardown_module
    download_folder = str(tmp_path)

    bucket.upload_file(test_file_path)
    bucket.download_file(os.path.basename(test_file_path), download_folder, "test_file_2.txt")

    file_path = os.path.join(download_folder, "test_file_2.txt")
    assert os.path.isfile(file_path)


def test_download_file_overwrite(setup_and_teardown_module, test_file_path, tmp_path):
    """
    Download files from bucket root folder into local temp folder, and rename with counter suffix if the
    file already exists

    test_file.txt -> test_file_2.txt
    """
    bucket = setup_and_teardown_module
    download_folder = str(tmp_path)

    bucket.upload_file(test_file_path)
    bucket.download_file(os.path.basename(test_file_path), download_folder)

    # Download the same files, but rename with counter suffix
    bucket.download_file(os.path.basename(test_file_path), download_folder, overwrite_local_file=False)

    file_path = os.path.join(download_folder, "test_file_2.txt")
    assert os.path.isfile(file_path)


def test_download_files_overwrite(setup_and_teardown_module, test_file_list_local, tmp_path):
    """
        Download all files provided by file list into the local temp folder, and rename with counter suffix if the
        file already exists

        test_file.txt -> test_file_2.txt
    """

    bucket = setup_and_teardown_module
    download_folder = str(tmp_path)

    upload_multi_files_folders(bucket, test_file_list_local)

    # Get listing of all files in the bucket and sub-folders
    file_list = bucket.get_file_list(recursive=True)

    # Download the files based on the list, but don't overwrite - rename with counter suffix
    bucket.download_files(file_list, download_folder, overwrite_local_file=False)
    assert bucket.file_count(recursive=True) == len(file_list)


def test_delete_file(setup_and_teardown_module, test_file_list_local):
    bucket = setup_and_teardown_module

    bucket.upload_files(test_file_list_local)

    # Get counting of all files in the bucket
    pre_file_count = bucket.file_count()
    bucket.delete_file(TEST_FILE_NAME)
    post_file_count = bucket.file_count()

    assert post_file_count == pre_file_count - 1

def test_delete_files(setup_and_teardown_module, test_file_list_local):
    bucket = setup_and_teardown_module

    upload_multi_files_folders(bucket, test_file_list_local)

    # Get listing of all files in the bucket and sub-folders that match regex
    file_list = bucket.get_file_list(file_match_regex=TEST_FILE_NAME, recursive=True)

    # Get counting of all files in the bucket
    pre_file_count = bucket.file_count(recursive=True)
    bucket.delete_files(file_list)
    post_file_count = bucket.file_count(recursive=True)

    assert post_file_count == pre_file_count - len(file_list)


def test_create_folder(setup_and_teardown_module):
    bucket = setup_and_teardown_module

    bucket.create_folder("test_folder_1")
    bucket.create_folder("test_folder_1/test_folder_1_1")

    # S3 search paths require folders to be suffixed with '/'
    assert bucket._object_exists("test_folder_1/")
    assert bucket._object_exists("test_folder_1/test_folder_1_1/")


def test_delete_folder(setup_and_teardown_module):
    bucket = setup_and_teardown_module

    bucket.create_folder("test_folder_1")
    bucket.create_folder("test_folder_1/test_folder_1_1")

    bucket.delete_folder("test_folder_1")
    bucket.delete_folder("test_folder_1/test_folder_1_1")

    # S3 search paths require folders to be suffixed with '/'
    assert not bucket._object_exists("test_folder_1/")
    assert not bucket._object_exists("test_folder_1/test_folder_1_1/")


# Helper functions
def upload_multi_files_folders(bucket, test_file_list_local):
    bucket.upload_files(test_file_list_local, "test_folder_1")
    bucket.upload_files(test_file_list_local, "test_folder_1/test_folder_1_1")
    bucket.upload_files(test_file_list_local, "test_folder_2")