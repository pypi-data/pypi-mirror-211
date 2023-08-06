# TODO: Add Unit Tests
# TODO: Add comments
import os
import re
from typing import List, Optional


def get_next_available_filename(file_path) -> str:
    base, ext = os.path.splitext(file_path)
    counter = 2

    while os.path.exists(file_path):
        file_path = f"{base}_{counter}{ext}"
        counter += 1

    return file_path


def file_path_is_valid(file_path: str) -> bool:
    """
    Check whether the provided file path is valid.

    This function checks whether the file path is not empty, is a directory,
    and whether the program has write permissions for it.

    Note: os.access may not always work as expected on some Unix systems.
    Python's os.access() checks using Python's effective user id/effective
    group id which may not always be the same as the real user id/group id,
    if the script is being run with elevated permissions (such as with sudo
    or setuid).

    :param file_path: The path of the file to check.
    :type file_path: str
    :return: True if the file path is valid, False otherwise.
    :rtype: bool

    :Example:

    >>> file_path_is_valid('/home/user/my_folder')
    True
    """
    return bool(file_path) and os.path.isdir(file_path) and os.access(file_path, os.W_OK)


def get_file_list(folder_path: str,
                  file_regex: Optional[str] = None,
                  folder_regex: Optional[str] = None,
                  recursive: Optional[bool] = False,
                  recursion_depth: Optional[int] = -1) -> List[str]:
    """
    Return a list of files in a local directory that match a certain regex pattern.

    :param folder_path: The path to the local directory.
    :type folder_path: str
    :param file_regex: Optional regex to filter the files. Default is None, which matches all files.
    :type file_regex: Optional[str]
    :param folder_regex: Optional regex to filter the folders during recursive search.
                         Default is None, which matches all folders.
    :type folder_regex: Optional[str]
    :param recursive: Whether to recursively traverse subfolders. Default is False.
    :type recursive: Optional[bool]
    :param recursion_depth: The maximum depth to recurse. -1 means no limit. Default is -1.
    :type recursion_depth: Optional[int]
    :return: A list of matching file paths.
    :rtype: List[str]
    """

    files = []

    # If we've hit the recursion limit, stop recursing
    if recursion_depth == 0:
        return files

    for item in os.scandir(folder_path):
        if item.is_file() and (file_regex is None or re.match(file_regex, item.name)):
            # This is a file, and it matches the file regex, and it can be read, so add it to the list
            if not os.access(item.path, os.R_OK):
                raise IOError(f"The local file {item.path} cannot be read.")

            files.append(item.path)
        elif item.is_dir() and recursive and (folder_regex is None or re.match(folder_regex, item.name)):
            # This is a directory, we're doing a recursive search, and it matches the folder regex
            files += get_file_list(item.path,
                                   file_regex,
                                   folder_regex,
                                   recursive,
                                   recursion_depth - 1 if recursion_depth > 0 else -1)

    return files
