import os

from django.conf import settings

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from packages.tasks import celery_generate_summary


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


@api_view(["post"])
def print_summary(request, start: str, end: str):

    output = celery_generate_summary(request, start, end)
    output.get()

    temp = "summary will be mailed soon as possible"

    return Response({"detail": temp}, status=status.HTTP_200_OK)
