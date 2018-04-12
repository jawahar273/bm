# from django.shortcuts import render

# Create your views here.
from django.core.cache import caches
from rest_framework import status

from weather2.tasks import celery_get_co_data


def get_air_pollution(request, weather_date, lat, lon):
    '''get the air quality data from the caches system
    or from the open weather api[beta api].

    :param request: default django request object
    :param weather_date: date get for getting the data from should
        with the 31 days from the last update from the services.
    :param lat: latitute of the user's.
    :param lon:  lontitute of the user's.

    ChangeLog:
        -- Thursday 12 April 2018 09:11:49 AM IST
            @jawahar273 [Version 0.1]
            -1- Init code

    '''
    result = {}
    CO_CACHES_NAME = 'airPollution_CO_%d_%d' % (lat, lon)
    SO2_CACHES_NAME = 'airPollution_SO2_%d_%d' % (lat, lon)
    caches_content = caches.get(CO_CACHES_NAME, None)

    if not caches_content:
        content_data = celery_get_co_data.delay(lat, lon).get(timeout=20)

        if content_data['code'] == status.HTTP_200_OK:

            #   To use open weather api more offen the
            #   expire time is set to midnight of th client
            #   location.

            #   set time for now
            confi_cache_timeout
            caches.set(CO_CACHES_NAME, content_data, )
    else:

        result['co'] = caches_content['data']
