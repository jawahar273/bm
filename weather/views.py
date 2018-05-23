import re
import datetime


from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


from weather.models import GAS_TYPE_CHOICES, AirPollutionData
from weather.serializers import AirPollutionDataSerializer
from weather.tasks import celery_update_air_pollution_db
from weather.exceptions import LatLonDoesNotExit, DateDoesNotExit


def air_pollution(weather_date=None, lat=None, lon=None):

    regex_format = settings.BM_REGEX_DATE_FORMAT

    if not re.search(regex_format, weather_date):

        return Response(
            {"detail": "wrong date format given"}, status=status.HTTP_400_BAD_REQUEST
        )

    date_format = settings.BM_STANDARD_DATEFORMAT
    weather_date = datetime.datetime.strptime(weather_date, date_format).date()

    response = {}

    for gtype in GAS_TYPE_CHOICES:

        gtype_code = gtype[0]
        queryset = AirPollutionData.objects.filter(
            data_base__location_lat=lat, data_base__location_lon=lon
        )

        if not queryset:

            raise LatLonDoesNotExit

        queryset = queryset.filter(weather_date=weather_date)

        if not queryset:

            raise DateDoesNotExit

        queryset = queryset.filter(data_base__gas_type=gtype_code)
        serializer = AirPollutionDataSerializer(data=queryset.values()[0])
        serializer.is_valid()
        response.update({gtype_code: serializer.data})

    return {"result": response}


@api_view(["get"])
def get_air_pollution(request, weather_date=None, lat=None, lon=None):

    delete_all = False
    result = None
    status_code = 0

    try:

        temp = air_pollution(weather_date, lat, lon)
        result = temp["result"]
        status_code = status.status.HTTP_200_OK

    except LatLonDoesNotExit:

        delete_all = False

    except DateDoesNotExit:

        delete_all = True

    output = celery_update_air_pollution_db.delay(lat, lon, delete_all)
    if isinstance(output.result, dict):
        result = output.result["msg"]
        status_code = output.result["code"]

        if status_code == status.HTTP_200_OK:
            get_air_pollution(request, weather_date, lat, lon)

    return Response(result, status=status_code)
