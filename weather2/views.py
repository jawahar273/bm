from datetime import datetime
import logging
import re

from django.conf import settings
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from weather2 import tasks as bm_celery

logger = logging.getLogger(__name__)


def set_caches(lat, lon, gcode_name, caches_name):
    '''set the caches to the server with
    data which is feached from the open weather
    (air pollution[beta api]).

    :param caches_name: the cache's name.
    :param gcode_name: gas type as code name.

    ChangeLog:
        -- Friday 13 April 2018 11:33:27 PM IST
            @jawahar273 [Version 0.1]
            -1- Init code.
        -- Friday 13 April 2018 11:44:08 PM IST
            @jawahar273 [Version 0.2]
            -1- converions the celery function to
            general callable form using using
            `__getattribute__`.
            -2- Update logger in the main else part.
    '''

    temp_celery = bm_celery.__getattribute__('celery_get_%s_data' % (gcode_name))
    data = temp_celery.delay(lat, lon).get(timeout=20)

    if data['code'] == status.HTTP_200_OK:

        #  If the day type is selected keep that it use the
        #  UTC for time zone.
        #  To make optimal use of
        #  the openweather api(air pollution[beta api]) set the cache type
        #  as date.
        confi_cache_timeout_type = settings.BM_WEATHER_DATA_CACHE_TYPE
        set_timeout = None

        if confi_cache_timeout_type == 'date':

            temp_date = datetime.strptime(data['time'],
                        settings.BM_ISO_8601_TIMESTAMP)

            set_timeout = datetime.now() - temp_date
            set_timeout = set_timeout.total_seconds()

        elif confi_cache_timeout_type == 'day':

            set_timeout = (24 - datetime.now().hour) * 3600

        #  days timeout code here
        cache.set(caches_name, data['content_data'], set_timeout)

    elif data['code'] == status.HTTP_500_INTERNAL_SERVER_ERROR:

        logger.error('Error in the celery data, No storing'
                     ' of the data in caches system')


def get_caches(caches_content, gcode_name):
    '''get the cache that is related to
    air pollution which is stored in the server
    by using the name of the caches.

    :param caches_content: the cache data(which is the dict of
        open weather (air pollution [beta api])).
    :param gcode_name: gas type as code name.
    :return: the cache object in python navtive form.
    :rtype: dict/list

    ChangeLog:
        -- Friday 13 April 2018 11:33:08 PM IST
            @jawahar273 [Version 0.1]
            -1- Init code
        -- Saturday 14 April 2018 11:56:05 AM IST
            @jawahar273 [Version 0.2]
            -1- update return value of this function.
    '''

    # get the time last update and todays date use that
    # as a sequance number to find the correct value in
    # data.
    last_upate = caches_content['time']
    last_upate = datetime.strptime(last_upate,
                                   settings.BM_ISO_8601_TIMESTAMP)
    num_days = (datetime.now() - last_upate).days

    if num_days > len(caches_content['data']):  # max_days count

        logger.error('Computated days should not exceed'
                     'the max_days count')

        return []

    return caches_content['data'][num_days]


@api_view(['get'])
def get_air_pollution(request, weather_date, lat, lon):
    '''get the air quality data from the caches system
    or from the open weather api[beta api].

    :param request: default django request object
    :param weather_date: date get for getting the data from should
        with the 31 days from the last update from the services.
    :param lat: latitute of the user's.
    :param lon:  lontitute of the user's.
    :rtype: Response

    ChangeLog:
        -- Thursday 12 April 2018 09:11:49 AM IST
            @jawahar273 [Version 0.1]
            -1- Init code
        -- Thursday 12 April 2018 11:18:11 PM IST
            @jawahar273 [Version 0.2]
            -1- Adding the timeout for new caches.
            -2- Date timeout has been done
        -- Friday 13 April 2018 09:34:05 PM IST
            @jawahar273 [Version 0.3]
            -1- Setting the cache for day.
            -2- Restrucuted the code to follow DRY rule as possible.
        -- Saturday 14 April 2018 12:39:05 PM IST
            @jawahar273 [Version 0.4]
            -1- Adding validation for date format.
    '''

    if not re.search(settings.BM_REGEX_DATE_FORMAT, weather_date):

        return Response({'detail': 'wrong date formate.'
                         ' Please Check date fromate'},
                        status=status.HTTP_400_BAD_REQUEST)
    CO_code_name = 'co'
    SO2_code_name = 'so2'
    result = {}

    CO_CACHES_NAME = 'airPollution_CO_%s_%s' % (lat, lon)
    SO2_CACHES_NAME = 'airPollution_SO2_%s_%s' % (lat, lon)

    CO_caches_content = cache.get(CO_CACHES_NAME, None)
    SO2_caches_content = cache.get(SO2_CACHES_NAME, None)

    status_code = status.HTTP_200_OK

    #  checking the caches is present or not
    if not CO_caches_content:

        # setting the caches
        set_caches(lat, lon, CO_code_name, CO_CACHES_NAME)

    else:

        result[CO_code_name] = get_caches(CO_caches_content,
                                          CO_code_name)
        logger.debug('setting the co result')

    #  checking the caches is present or not
    if not SO2_caches_content:

        set_caches(lat, lon, SO2_code_name, SO2_CACHES_NAME)

    else:

        result[SO2_code_name] = get_caches(SO2_caches_content,
                                           SO2_code_name)
        logger.debug('setting the so2 result')

    #  Checking the content is present on both.
    if not result.get(CO_code_name) and not result.get(SO2_code_name):

        #  this is used, that celery is async task
        #  which they may or may not return data suddenly,
        #  so we are computing after little time out.

        CO_caches_content = cache.get(CO_CACHES_NAME)
        SO2_caches_content = cache.get(SO2_CACHES_NAME)

        result[CO_code_name] = get_caches(CO_caches_content,
                                          CO_code_name)

        result[SO2_code_name] = get_caches(SO2_caches_content,
                                           SO2_code_name)
    return Response({'detail': result},
                    status=status_code)
