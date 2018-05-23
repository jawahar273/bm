import re
import datetime

from django.conf import settings


def flatter_list(items):
    """
     fastest way to flatten list of elements
     Eg: [(1, 2), (2, 45)] => [1, 2, 2, 45]
    """
    return [item for sublist in items for item in sublist]


def to_hexdigit(name):
    """
    Get the name and conver to md5 string.

    @params name get the name.
    """
    from hashlib import md5

    return md5(name.encode()).hexdigest()


def to_hrs(mins=0, secs=0, time_format=False) -> str:
    """
    Convert the given minutes or seconds into hours.

    @params mins time in minus.
    @params secs time in secs.
    @params time_format is to return the time format.
    """
    assert not (mins > 0 and secs > 0), (
        "Both the mins and secs as arguments" "are not allowed"
    )
    if secs > 0:
        mins, secs = divmod(secs, 60)
    hrs, mins = divmod(mins, 60)
    if time_format:
        return "%d:%02d:%02d" % (hrs, mins, secs)
    return "%d" % (hrs)


def to_percentage(current_value, total_value):

    return int((current_value / total_value) * 100)


def validate_bm_standard_date_format(value):
    """This function which help in
    validate the given date with BM standard date.

    :params value (str): date in string
    :return: where is given format is valide or not
    :rtype: bool
    """

    regex_date = settings.BM_REGEX_DATE_FORMAT
    return re.search(regex_date, value)


def validate_less_than_today(value):
    """This function which help in validate
    the given date less than today.
    """

    if not validate_bm_standard_date_format(value):
        return False

    today = datetime.date.today()
    # need implement


def to_query_string_dict(value):

    content = {}
    value = value.decode("utf-8")
    value = value.split(",")
    for inx in value:
        inx = inx.split("=")
        content[inx[0]] = inx[1]

    return content
