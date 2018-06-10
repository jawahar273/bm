import re
import datetime
from typing import List, Dict

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader

from bm.users.utils import to_datetime_format


def flatter_list(items: List[List[any]]) -> List[any]:
    """
     fastest way to flatten list of elements
     Eg: [(1, 2), (2, 45)] => [1, 2, 2, 45]
    """
    return [item for sublist in items for item in sublist]


def to_hexdigit(name: str) -> str:
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


def to_percentage(current_value, total_value) -> int:

    return int((current_value / total_value) * 100)


def validate_bm_standard_date_format(value: str) -> bool:
    """This function which help in
    validate the given date with
    BM standard date.

    :params value (str): date in string
    :return: where is given format is valide or not
    :rtype: bool
    """

    regex_date = settings.BM_REGEX_DATE_FORMAT
    return re.search(regex_date, value)


def validate_less_than_today(value: str) -> bool:
    """This function which help in validate
    the given date less than today.

    ChangeLog:
        --Sunday 27 May 2018 11:44:47 PM IST
        @jawahar273 [Version 0.2]
        -1- Init Code.
    """

    if not validate_bm_standard_date_format(value):

        raise ValueError("Given date format is wrong")

    today = datetime.datetime.today()
    date_format = settings.BM_STANDARD_DATEFORMAT
    date_given = to_datetime_object(value, date_format)
    lowest_year = settings.BM_LOWEST_YEAR_POSSIBLE

    if date_given >= today and lowest_year < date_given:

        return False

    return True


def to_query_string_dict(value: bytes) -> Dict:

    content = {}
    value = value.decode("utf-8")
    value = value.split(",")

    for inx in value:

        inx = inx.split("=")
        content[inx[0]] = inx[1]

    return content


def find_dict_value(key_word: str, _items: Dict) -> any:

    for key, value in _items.items():

        if key_word == value:

            return key


def start_and_end_month(month: int, operation: str, date_format: str):
    """This function from the
    before or after current month.

    :param month: [month of generate the eange]
    :type month: int
    :param operation: [before and after range of moths]
    :type operation: [str]
    :param date_format: datetiem format for time object.
    :type date_format: [str]

    ChangeLog:
        --Saturday 09 June 2018 01:12:39 PM IST
        @jawahar273 [Version 0.1]
        -1- Init Code.
        --Saturday 09 June 2018 05:16:36 PM IST
        @jawahar273 [Version 0.2]
        -1- New param datetime.
        -2- Update in code structure.
    """
    temp = None
    if operation == "after":

        temp = datetime.date.today() + datetime.timedelta(month * 365 / 12)

    elif operation == "before":

        temp = datetime.date.today() - datetime.timedelta(month * 365 / 12)

    return to_datetime_format(temp, date_format)


def start_month_year(month: int, operation: str, date_format=None):
    """This function is built on the top
    of the .. function:: start_and_end_month()
    to provied high level custom
    return date.

    @ref:: `start_and_end_month`

    ChangeLog:
        --Saturday 09 June 2018 01:12:39 PM IST
        @jawahar273 [Version 0.1]
        -1- Init Code.
        --Saturday 09 June 2018 05:17:38 PM IST
        @jawahar273 [Version 0.2]
        -1- New param datetime.
    """
    if not date_format:

        date_format = settings.BM_STANDARD_START_MONTH_FORMAT

    temp = start_and_end_month(month, operation, date_format)

    return temp


def sending_mail_pdf(mail_to: List[str], file_pointer=None) -> None:
    """Sending mail with the summary
    PDF attachment.

    :param mail_to: [recetion to send based on the register mail]
    :type mail_to: [list]
    :param file_pointer: [file pointer to pdf.]
    :type file_pointer: [any]


    ChangLog:
        -- Friday 08 June 2018 06:45:10 PM IST
        @jawahar273 [Version 0.1]
        -1- Init code.
        -- Friday 08 June 2018 10:55:26 PM IST
        @jawahar273 [Version 0.2]
        -1- Sending the mail even if the file
        pointer is `None`.
    """

    subject = "Expensive attachment from"
    load_template = loader.get_template(settings.BM_MAIL_SUMMARY_TEMPLATE)

    mail = EmailMultiAlternatives(
        subject, load_template.render(), settings.DEFAULT_FROM_EMAIL, mail_to
    )

    mail.attach_file(file_pointer.read(), "application/pdf")

    mail.send()
