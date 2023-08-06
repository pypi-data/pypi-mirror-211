# TODO: Add Unit Tests
# A SharePoint convenience wrapper around python-o365 library - https://github.com/O365/python-o365
# Source reference
#   https://github.com/O365/python-o365/blob/master/O365/sharepoint.py
# See examples/sharepoint folder for usage scenarios

import os
from multiprocessing import AuthenticationError
from pathlib import Path
from typing import Tuple

from O365 import Account
from O365.drive import Drive, Folder
from O365.sharepoint import Sharepoint, Site


def get_sharepoint(client_id: str, client_secret: str, tenant_id: str) -> Sharepoint:
    """
    Authenticates and retrieves a SharePoint instance.

    :param client_id: The client ID for authentication.
    :type client_id: str
    :param client_secret: The client secret for authentication.
    :type client_secret: str
    :param tenant_id: The tenant ID for the SharePoint account.
    :type tenant_id: str
    :returns: An authenticated SharePoint instance.
    :rtype: Sharepoint
    :raises TypeError: If any of the inputs are not strings.
    :raises AuthenticationError: If there is an issue with authentication.

    """
    # Type checking
    if not all(isinstance(i, str) for i in [client_id, client_secret, tenant_id]):
        raise TypeError("All inputs must be strings.")

    try:
        credentials: Tuple[str, str] = (client_id, client_secret)

        account = Account(credentials, auth_flow_type='credentials', tenant_id=tenant_id)
        account.authenticate()

        return account.sharepoint()
    except Exception as e:
        raise AuthenticationError("There was an issue with authentication.") from e


def get_site_from_sharepoint(sharepoint: Sharepoint, host: str, site_name: str) -> Site:
    # The get_site call expects the spaces to be stripped out of name for lookup purposes
    return sharepoint.get_site(host, 'sites/' + site_name.replace(" ", ""))


def get_document_library_from_site(site: Site, document_library_name: str) -> Drive or None:
    """
    Searches for a specific document library in a given SharePoint site.

    :param site: The SharePoint site to search in.
    :type site: Site
    :param document_library_name: The name of the document library to search for.
    :type document_library_name: str
    :returns: The found document library if it exists, else None.
    :rtype: Drive or None
    """
    # Iterate over document libraries in the site
    for doc_lib in site.list_document_libraries():
        # Return the document library if the name matches
        if doc_lib.name == document_library_name:
            return doc_lib

    # Return None if no matching document library is found
    return None


def get_document_library(client_id: str, client_secret: str, tenant_id: str, host: str, site_name: str,
                         document_library_name: str) -> Drive or None:
    sharepoint = get_sharepoint(client_id, client_secret, tenant_id)
    site = get_site_from_sharepoint(sharepoint, host, site_name)

    return get_document_library_from_site(site, document_library_name)


def get_folder_items(folder: Folder or Drive) -> list:
    return folder.get_items()


def get_child_files(parent_folder: Folder or Drive) -> list:
    files = []

    for item in get_folder_items(parent_folder):
        if not item.is_folder:
            files.append(item)

    return files


def get_child_folders(parent_folder: Folder or Drive) -> list:
    folders = []

    for item in get_folder_items(parent_folder):
        if item.is_folder:
            folders.append(item)

    return folders


def get_folder(document_library: Drive, folder_path: str or Path) -> Folder or Drive:
    return document_library.get_item_by_path(folder_path)


def get_child_folder(parent_folder: Folder or Drive, name: str) -> Folder or None:
    for parent_folder in parent_folder.get_child_folders():
        if parent_folder.name == name:
            return parent_folder

    return None


def create_folder(document_library: Drive, parent_folder_path: str or Path, name: str) -> Folder:
    # Based on path from doc library, create a folder given a parent path and folder name
    folder = get_folder(document_library, parent_folder_path)
    return create_child_folder(folder, name)


def create_child_folder(parent_folder: Folder or Drive, name: str) -> Folder:
    """
    Creates a child folder under the given parent folder. If the folder already exists, returns the existing one.

    :param parent_folder: The parent folder under which the child folder should be created. This can be a Folder or Drive.
    :type parent_folder: Folder or Drive
    :param name: The name of the child folder to be created.
    :type name: str
    :returns: The newly created or existing child folder.
    :rtype: Folder
    """
    # If the folder already exists, return it
    child_folder = get_child_folder(parent_folder, name)
    if child_folder is not None:
        return child_folder

    # If parent_folder is a Drive, get its root folder
    if isinstance(parent_folder, Drive):
        parent_folder = parent_folder.get_root_folder()

    # Create the child folder
    return parent_folder.create_child_folder(name)


def rebuild_child_folder(parent_folder: Folder or Drive, name: str) -> Folder:
    child_folder = get_child_folder(parent_folder, name)

    if child_folder:
        delete_folder(child_folder)

    return create_child_folder(parent_folder, name)


def delete_folder(folder: Folder):
    # Recursive deletion of containing files/folders, then proceed to folder
    folder_items = get_folder_items(folder)
    for item in folder_items:
        if item.is_folder:
            delete_folder(item)
        else:
            item.delete()

    folder.delete()


def upload_file(folder: Folder or Drive, source_file_path: str, target_file_name: str = None):
    if isinstance(folder, Drive):
        folder = folder.get_root_folder()

    folder.upload_file(source_file_path, target_file_name)


def upload_files(folder: Folder or Drive, source_folder_path: str):
    for root, dirs, files in os.walk(source_folder_path):
        for file in files:
            # Get the full path of the file
            source_file_path = os.path.join(root, file)
            upload_file(folder, source_file_path, file)
