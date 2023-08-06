# TODO: Add Unit Tests
# TODO: Add comments
# An Exchange convenience wrapper around python-o365 library - https://github.com/O365/python-o365
# Source reference
# - https://github.com/O365/python-o365/blob/master/O365/mailbox.py
# - https://github.com/O365/python-o365/blob/master/O365/message.py
# Message properties
# - https://learn.microsoft.com/en-us/graph/api/resources/message?view=graph-rest-1.0
# - https://learn.microsoft.com/en-us/graph/filter-query-parameter?tabs=http
# Common Message Properties
# - Message body -> body/content
# - From address -> from/emailAddress/address
# - Message subject -> subject
# - Message received Datetime -> receivedDatetime
# - Message send Datetime -> sendDatetime
# - Is read flag -> isRead
# See examples/exchange folder for usage scenarios

import re
import time
from typing import Optional

from O365 import Account
from O365.mailbox import MailBox, Folder, Message


def delete_message(message: Message):
    message.delete()


def get_mailbox(client_id: str, client_secret: str, tenant_id: str, mailbox_address: str) -> MailBox:
    credentials = (client_id, client_secret)

    account = Account(credentials, auth_flow_type='credentials', tenant_id=tenant_id)
    account.authenticate()

    return account.mailbox(mailbox_address)


def get_inbox(mailbox: MailBox) -> Folder:
    return mailbox.inbox_folder()


def get_folder(mailbox: MailBox, folder_name: str) -> Folder:
    return mailbox.get_folder(folder_name=folder_name)


def get_message_in_folder(folder: Folder, query_filter: str, order_by: Optional[str] = None, timeout: int = 30) -> \
        Optional[Message]:
    """
    Retrieves a single message from a given folder that meets specified filter criteria.

    This function attempts to retrieve a message within a specified timeout period.
    If no message is found that meets the filter criteria within the timeout period, the function returns None.

    :param folder: The folder from which to retrieve the message
    :type folder: Folder
    :param query_filter: The filter criteria for the message
    :type query_filter: str
    :param order_by: The order by which to sort the messages, defaults to None
    :type order_by: str, optional
    :param timeout: The number of seconds to keep attempting to retrieve a message, defaults to 30
    :type timeout: int, optional
    :return: The message that meets the filter criteria, or None if no message is found within the timeout period
    :rtype: Message, optional
    """
    # Calculate the end time based on the current time and the specified timeout
    end_time = time.time() + float(timeout)

    # Define the wait interval between attempts to retrieve a message
    interval = 1

    # Keep attempting to retrieve a message until the timeout is reached
    while time.time() < end_time:
        try:
            # Try to retrieve a single message that meets the filter criteria
            messages = get_messages_in_folder(folder, query_filter, order_by, 1)
            message = next(messages)

            # If a message is retrieved, return it
            return message
        except StopIteration:
            # If no messages meet the filter criteria, wait for the interval before trying again
            time.sleep(interval)

    # If the timeout is reached without retrieving a message, return None
    return None


def get_messages_in_folder(folder: Folder, query_filter: str, order_by: str = None, limit: int = 30) -> list:
    # See the following for guidance construction of order-by clauses
    # https://learn.microsoft.com/en-us/graph/api/user-list-messages?view=graph-rest-1.0&tabs=http#using-filter-and-orderby-in-the-same-query
    # Example
    # - query_filter = 'from/emailaddress/address eq test@company.com'
    # - order_by = 'from/emailAddress/address,sentDateTime desc'

    return folder.get_messages(query=query_filter, order_by=order_by, limit=limit)


def get_value_from_subject(message: Message, extract_regex) -> str:
    subject = message.subject()
    matches = re.findall(extract_regex, subject)

    return matches[0] if matches else None


def get_value_from_body(message: Message, extract_regex: str) -> str:
    body = message.get_body_text()
    matches = re.findall(extract_regex, body)

    return matches[0] if matches else None


def send_message(mailbox: MailBox, subject: str, body: str, to: list, sender: str) -> Message:
    """
    Composes and sends a new message from a given mailbox.

    This function creates a new message in the drafts folder, sets the required fields (subject, body, sender, and recipients),
    sends the message, and then returns the sent message.

    :param mailbox: The mailbox from which the message is sent
    :type mailbox: MailBox
    :param subject: The subject of the message
    :type subject: str
    :param body: The body of the message
    :type body: str
    :param to: The list of recipients for the message
    :type to: list
    :param sender: The sender of the message
    :type sender: str
    :return: The sent message
    :rtype: Message
    """
    # Get the drafts folder from the mailbox
    drafts_folder = mailbox.drafts_folder()

    # Create a new message in the drafts folder
    message = drafts_folder.new_message()

    # Set the subject, body, and sender of the message
    message.subject = subject
    message.body = body
    message.sender = sender

    # Add each recipient in the 'to' list to the message's recipients
    for recipient in to:
        message.to.add(recipient)

    # Send the message
    message.send()

    # Return the sent message
    return message
