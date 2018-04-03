import re
import datetime


from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


from weather.models import (GAS_TYPE_CHOICES,
                            AirPollutionData)
from weather.serializers import AirPollutionDataSerializer
from weather.tasks import celery_update_air_pollution_db
from weather.exceptions import LatLonDoesNotExit, DateDoesNotExit


def air_pollution(weather_date=None, lat=None, lon=None):

    regex_format = settings.BM_REGEX_DATE_FORMAT

    if not re.search(regex_format, weather_date):

        return Response({'detail': 'wrong date format given'},
                        status=status.HTTP_400_BAD_REQUEST)

    date_format = settings.BM_STANDARD_DATEFORMAT
    weather_date = datetime.datetime.strptime(weather_date,
                                              date_format).date()

    response = {}

    for gtype in GAS_TYPE_CHOICES:

        gtype_code = gtype[0]
        queryset = AirPollutionData.objects.filter(location_lat=lat,
                                                   location_lon=lon)

        if not queryset:

            raise LatLonDoesNotExit

        queryset = queryset.filter(weather_date=weather_date)

        if not queryset:

            raise DateDoesNotExit

        queryset = queryset.filter(data_base__gas_type=gtype_code)
        serializer = AirPollutionDataSerializer(data=queryset.values()[0])
        serializer.is_valid()
        response.update({gtype_code: serializer.data})

    return Response({'detail': response}, status=status.HTTP_200_OK)


@api_view(['get'])
def get_air_pollution(request, weather_date=None, lat=None, lon=None):

    delete_all = False

    try:

        return air_pollution(weather_date, lat, lon)

    except LatLonDoesNotExit:

        delete_all = False

    except DateDoesNotExit:

        delete_all = True

    output = celery_update_air_pollution_db.delay(lat,
                                                  lon,
                                                  delete_all)
    output.ready()

    return Response([], status=status.HTTP_200_OK)
