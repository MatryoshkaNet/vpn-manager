import datetime


def get_server_now() -> datetime.datetime:
    """
    Return the current date and time in UTC.

    This function provides a consistent UTC timestamp for the application,
    suitable for logging, database storage, and other time-sensitive operations.

    :returns: The current UTC date and time with tzinfo set to UTC.
    :rtype: datetime.datetime
    """
    return datetime.datetime.now(datetime.UTC)
