import datetime
import importlib
from django.core.cache import cache
from django.conf import settings


def to_datetime_format(date, date_format: str) -> str:
    """converting the date object into
    given date format.

    :param date: [description]
    :type date: [datetime.datetime]
    :param date_format: [description]
    :type date_format: [str]
    :returns: [description]
    :rtype: {[str]}
    """
    try:

        return datetime.datetime.strftime(date, date_format)

    except ValueError as e:

        return None


def to_datetime_object(date: str, date_format: str) -> datetime.datetime:
    """converting the date format  into
    given date object.

    :param date: [date]
    :type date: [str]
    :param date_format: [date format]
    :type date_format: [str]
    :returns: [description]
    :rtype: {[datetime.datetime]}

    ChangeLog:
        --Sunday 27 May 2018 11:44:28 PM IST
        @jawahar273 [Version 0.1]
        -1- Init Code.
    """
    try:

        return datetime.datetime.strptime(date, date_format)

    except ValueError as e:

        return None


def import_class(value):
    """Import the given class based on string.

    :param value: [path of the class]
    :type value: [str]
    :returns: [class object]
    :rtype: {[Object]}
    """
    value, class_name = value.rsplit(".", 1)
    module = importlib.import_module(value)
    return getattr(module, class_name)


def set_cache(name: str, data: any, timeout=90):

    cache.set(name, data, timeout)


def get_cache(name: str) -> any:

    return cache.get(name)
