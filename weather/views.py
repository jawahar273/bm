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

        _queryset = AirPollutionData.objects.filter(data_base__gas_type=gtype_code,
                                                    weather_date=weather_date)


        serializer = AirPollutionDataSerializer(data=_queryset.values()[0])
        serializer.is_valid()
        response.update({gtype_code: serializer.data})

    return Response({'detail': response}, status=status.HTTP_200_OK)


@api_view(['get'])
def get_air_pollution(request, weather_date=None, lat=None, lon=None):

    try:
        return air_pollution(weather_date, lat, lon)
    except IndexError:
        output = celery_update_air_pollution_db.delay(lat, lon)
        output.ready().get(timeout=10)
        return Response([], status=status.HTTP_200_OK)


# class AirPollutionView(viewsets.ReadOnlyModelViewSet):

#     queryset = AirPollution.objects.all()
#     serializer_class = AirPollutionDataSerializer
#     lookup_field = ('weather_date', 'lat', 'lon', )

#     def retrieve(self, request, weather_date=None, lat=None, lon=None):

#         regex_format = settings.BM_REGEX_DATE_FORMAT

#         if not re.search(regex_format, weather_date):
#             return Response({'detail': 'wrong date format given'},
#                             status=status.HTTP_400_BAD_REQUEST)

#         date_format = settings.BM_STANDARD_DATEFORMAT
#         weather_date = datetime.datetime.strptime(weather_date,
#                                                   date_format).date()

#         response = {}

#         for gtype in GAS_TYPE_CHOICES:

#             gtype_code = gtype[0]

#             _queryset = AirPollutionData.objects.filter(data_base__gas_type=gtype_code,
#                                                         weather_date=weather_date)

#             try:

#                 serializer = AirPollutionDataSerializer(data=_queryset.values()[0])
#                 serializer.is_valid()
#                 response.update({gtype_code: serializer.data})

#             except IndexError:
#                 return Response([], status=status.HTTP_200_OK)

#         return Response({'detail': response}, status=status.HTTP_200_OK)
