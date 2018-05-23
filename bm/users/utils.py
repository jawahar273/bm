import datetime as datetime
import importlib


def to_date_format(date, date_format):
    """converting the date object into
    given date format.

    :param date: [description]
    :type date: [datetime.datetime]
    :param date_format: [description]
    :type date_format: [str]
    :returns: [description]
    :rtype: {[str]}
    """
    return datetime.datetime.strftime(date, date_format)


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
