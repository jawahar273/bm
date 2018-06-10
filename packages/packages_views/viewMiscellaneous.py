import os
import datetime
import calendar
import logging

from typing import Dict

from django.conf import settings

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from packages.tasks import celery_generate_summary
from packages.utils import start_month_year

from bm.users.utils import to_datetime_object, to_datetime_format, get_cache, set_cache

logger = logging.getLogger(__name__)


@api_view(["get"])
def get_currency(request):
    """
     get the currency symbole and representation from json
    """

    import json

    file_location = os.path.join(settings.STATIC_ROOT, "js", "")
    file_location += settings.BM_CURRENCY_DETAIL_JSON_FILE

    with open(file_location) as file:

        return Response(json.loads(file.read()), status=status.HTTP_200_OK)


def print_summary_config() -> Dict:

    current = datetime.datetime.now()
    start_date = to_datetime_format(current, settings.BM_STANDARD_START_MONTH_FORMAT)

    last_date = calendar.monthrange(current.year, current.month)
    # HACK: no need for consier in date format
    # as the date for this specific case always
    # has two digit, no problem will occures.
    last_date = "%d-%d-%d" % (current.year, current.month, last_date[1])

    temp = {
        "current_month": {"start": start_date, "end": last_date},
        "two_months": {"start": start_month_year(2, "before"), "end": last_date},
        "three_months": {"start": start_month_year(3, "before"), "end": last_date},
        "six_months": {"start": start_month_year(6, "before"), "end": last_date},
    }

    return temp


@api_view(["get"])
def print_summary_key(request):

    cache_name = "print_summary_key"
    temp = get_cache(cache_name)
    if not temp:

        set_timeout = (24 - datetime.datetime.now().hour) * 3600
        temp = print_summary_config().keys()
        # PLAN: handle exception on the cache.

        try:

            temp = list(temp)
            set_cache(cache_name, temp, set_timeout)

        except TypeError as type_error:

            logger.error("Unable to set cache as {}".format(type_error))
            logger.debug("Unable to set cache as {}".format(type_error))

    return Response({"detail": temp}, status=status.HTTP_200_OK)


@api_view(["post"])
def print_summary(request, key_value: str):
    """This function will get the param
    and verfies with the .. function:: print_summary_config()

    :param request: [request object from djagno ]
    :type request: [request]
    :param range_value: [key from .. function:: print_summary_config()]
    :type range_value: [str]
    :returns: [Simple message to the user]
    :rtype: {[Response]}
    """
    temp = print_summary_config()
    output = celery_generate_summary(request, temp[key_value])
    output.get()

    temp = "summary will be mailed soon as possible"

    return Response({"detail": temp}, status=status.HTTP_200_OK)
