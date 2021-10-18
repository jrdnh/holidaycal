from datetime import datetime
from dateutil.relativedelta import relativedelta


def weekend_to_monday(dt: datetime) -> datetime:
    """
    If date falls on a Saturday or Sunday, return the following Monday.
    """
    if dt.weekday() == 5:
        return dt + relativedelta(days=2)
    if dt.weekday() == 6:
        return dt + relativedelta(days=1)
    return dt


def weekend_to_friday(dt: datetime) -> datetime:
    """
    If date falls on a Saturday or Sunday, return the previous Friday.
    """
    if dt.weekday() == 5:
        return dt - relativedelta(days=1)
    if dt.weekday() == 6:
        return dt - relativedelta(days=2)
    return dt


def nearest_weekday(dt: datetime) -> datetime:
    """
    If date falls on a Saturday, return previous Friday.
    If date falls on a Sunday, return following Monday.
    """
    if dt.weekday() == 5:
        return dt - relativedelta(days=1)
    if dt.weekday() == 6:
        return dt + relativedelta(days=1)
    return dt


def sunday_to_monday(dt: datetime) -> datetime:
    """
    If date falls on a Sunday, return following Monday
    """
    if dt.weekday() == 6:
        return dt + relativedelta(days=1)
    return dt


def saturday_to_friday(dt: datetime) -> datetime:
    """
    If date falls on a Saturday, return previous Friday
    """
    if dt.weekday() == 5:
        return dt - relativedelta(days=1)
    return dt


def sunday_to_tuesday(dt: datetime) -> datetime:
    """
    If date falls on a Sunday, return following Tuesday (e.g. UK Boxing day)
    """
    if dt.weekday() == 6:
        return dt + relativedelta(days=2)
    return dt
