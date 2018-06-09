import os
import datetime
import calendar

from django.conf import settings

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from packages.tasks import celery_generate_summary
from packages.utils import start_month_year


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


def print_summary_config():

    current = datetime.datetime.now()
    start_date = "01-%d-%d" % (current.month, current.year)

    last_date = calendar.monthrange(current.year, current.month)
    last_date = "%d-%d-%d" % (last_date[1], current.month, current.year)

    temp = {
        "current_month": (start_date, last_date),
        "two_months": (start_month_year(2, "before"), last_date),
        "three_months": (start_month_year(3, "before"), last_date),
        "six_months": (start_month_year(6, "before"), last_date),
    }

    return temp


@api_view(["get"])
def print_summary_range(request):

    temp = print_summary_config()

    return Response({"detail": temp}, status=status.HTTP_200_OK)


@api_view(["post"])
def print_summary(request, range_value: str):

    output = celery_generate_summary(request, start, end)
    output.get()

    temp = "summary will be mailed soon as possible"

    return Response({"detail": temp}, status=status.HTTP_200_OK)
