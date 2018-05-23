import datetime.datetime as datetime


def to_date_format(date, date_format):
    """converting the date object into
    given date format.

    [description]
    :param date: [description]
    :type date: [datetime.datetime]
    :param date_format: [description]
    :type date_format: [str]
    :returns: [description]
    :rtype: {[str]}
    """
    return datetime.strftime(date, date_format)
