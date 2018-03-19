import re


from django.conf import settings

from rest_framework import viewsets, status
from rest_framework.response import Response


from weather.models import GAS_TYPE_CHOICES, AirPollution, AirPollutionData
from weather.serializers import (AirPollutionSerializer,
                                 AirPollutionDataSerializer)


class AirPollutionView(viewsets.ReadOnlyModelViewSet):

    queryset = AirPollution.objects.all()
    serializer_class = AirPollutionSerializer

    def retrieve(self, request, date=None):
        '''
        :param: request
        :param str date: get the value from db based on date.

        '''

        regex_date = settings.REGEX_DATE_FORMAT

        if not re.search(regex_date, date):
            return Response({'detail': 'wrong date format given'},
                            status=status.HTTP_400_BAD_REQUEST)
        response = []

        for gtype in GAS_TYPE_CHOICES:

            gtype_code = gtype[0].lower()
            _queryset = AirPollutionData.objects.filter(data_base__gas_type=gtype_code,
                                                        weather_date=date)

            _serializer = AirPollutionDataSerializer(data=_queryset)
            _serializer.is_valid()
            response.append(_serializer.data)

        return Response({'detail': response}, status=status.HTTP_200_OK)

