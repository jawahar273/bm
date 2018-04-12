import datetime

from django.conf import settings
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
        -- Thursday 12 April 2018 11:18:11 PM IST
            @jawahar273 [Version 0.2]
            -1- Adding the timeout for new caches.
            -2- Date timeout has been done

    '''
    result = {}
    CO_CACHES_NAME = 'airPollution_CO_%d_%d' % (lat, lon)
    SO2_CACHES_NAME = 'airPollution_SO2_%d_%d' % (lat, lon)
    caches_content = caches.get(CO_CACHES_NAME, None)

    if not caches_content:
        data = celery_get_co_data.delay(lat, lon).get(timeout=20)

        if data['code'] == status.HTTP_200_OK:

            #  If the day type is selected keep that it use the
            #  UTC for time zone.
            #  To make optimal use of
            #  the openweather api(air pollution[beta api]) set the cache type
            #  as date.
            confi_cache_timeout_type = settings.BM_WEATHER_DATA_CACHE_TYPE
            set_timeout = None

            if confi_cache_timeout_type == 'date':
                temp_date = datetime.datetime.strptime(data['time'],
                            settings.BM_ISO_8601_TIMESTAMP)

                set_timeout = datetime.datetime.now() - temp_date
                set_timeout = set_timeout.total_seconds()

            #  days timeout code here
            caches.set(CO_CACHES_NAME, data, set_timeout)
    else:

        result['co'] = caches_content['data']
