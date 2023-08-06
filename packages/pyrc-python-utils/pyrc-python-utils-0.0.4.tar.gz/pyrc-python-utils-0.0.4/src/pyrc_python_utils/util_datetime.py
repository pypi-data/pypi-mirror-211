# TODO: Add Unit Tests
# TODO: Add comments
from datetime import datetime, timedelta


def get_utc_now(offset_minutes: int) -> str:
    """
    Returns the current UTC time adjusted by a specified offset.

    This function is useful, for example, when filtering emails based on their timestamp properties (such as sentDatetime).
    If the filter is being applied shortly after the email was sent, it might be useful to adjust the time a few minutes
    back from the current time.

    Parameters:
    offset_minutes (int): The number of minutes to offset the current UTC time by.

    Returns:
    str: The adjusted UTC time in the format '%Y-%m-%dT%H:%M:%S.%fZ'.
    """

    # Get the current UTC time
    current_utc_time = datetime.utcnow()

    # Adjust the current UTC time based on the specified offset
    adjusted_utc_time = current_utc_time + timedelta(minutes=offset_minutes)

    # Return the adjusted UTC time as a string formatted according to the ISO 8601 standard,
    # but with the last 3 digits of the microseconds removed. The 'Z' at the end represents the zero UTC offset.
    return adjusted_utc_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
