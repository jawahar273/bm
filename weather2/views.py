from datetime import datetime
import logging
import re

from django.conf import settings
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from weather2 import tasks as bm_celery
from weather2.utils import empty_gas_type

logger = logging.getLogger(__name__)


def get_openweather_data(lat, lon, gcode_name):
    '''Get the openweather air pollution data.
       See also :class: `.set_caches_redis`.
    :return: async result of celery
    :rtype: :class: `.celery.result.AsyncResult`.

    ChangeLog:
        -- Friday 04 May 2018 07:36:58 PM IST
            @jawahar273 [Version 0.1]
            -1- Init Code.
            -2- return async result celery.
    '''
    _celery = bm_celery.__getattribute__('celery_get_%s_data' % (gcode_name))
    return _celery.delay(lat, lon).get(timeout=20)


def get_count_days(last_upate):
    '''Get the days count between today and
    last update(in openweather api) datetimestramp.

    :param last_upate: [date in string]
    :type last_upate: [str]

    ChangeLog:
        -- Friday 04 May 2018 08:50:08 PM IST
            @jawahar273 [Version 0.1]
            -1- Init Code.
            -2- return async result celery.
    '''

    last_upate = datetime.strptime(last_upate,
                                   settings.BM_ISO_8601_TIMESTAMP)
    return (datetime.now() - last_upate).days - 1


def set_caches_redis(lat, lon, gcode_name, caches_name):
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
        -- Friday 04 May 2018 09:10:46 PM IST
            @jawahar273 [Version 0.3]
            -1- adding new variable.
    '''

    # get the weather data from the openweather.
    data = get_openweather_data(lat, lon, gcode_name)

    if data['code'] == status.HTTP_200_OK:

        #  If the day type is selected keep that it use the
        #  UTC for time zone.
        #  To make optimal use of
        #  the openweather api(air pollution[beta api]) set the cache type
        #  as date.
        confi_cache_timeout_type = settings.BM_WEATHER_DATA_CACHE_TYPE
        set_timeout = None

        if confi_cache_timeout_type == 'date':
            temp_time = settings.BM_ISO_8601_TIMESTAMP
            temp_date = datetime.strptime(data['time'], temp_time)

            set_timeout = datetime.now() - temp_date
            set_timeout = set_timeout.total_seconds()

        elif confi_cache_timeout_type == 'day':

            set_timeout = (24 - datetime.now().hour) * 3600

        #  days timeout code here
        cache.set(caches_name, data['content_data'], set_timeout)

    elif data['code'] == status.HTTP_500_INTERNAL_SERVER_ERROR:

        logger.error('Error in the celery data, Nothing is stored'
                     ' of the data in caches system')
    else:

        logger.error('Error in the celery data. May the reason:' + data)


def get_caches_redis(caches_content, gcode_name):
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

    num_days = get_count_days(caches_content['time'])

    if num_days >= len(caches_content['data']):  # max_days count

        logger.error('Computated days should not exceed'
                     ' the max_days count. Last update date'
                     ' {}, Gas Type: {}'
                     ' '.format(caches_content['time'],
                                gcode_name))

        return empty_gas_type()

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
        -- Friday 04 May 2018 08:57:27 PM IST
            @jawahar273 [Version 1.0]
            -1- Update code with cache and non cache system.
        -- Saturday 05 May 2018 04:27:04 PM IST
            @jawahar273 [Version 1.1]
            -1- fixing the bug.(syntax error)

    '''

    if not re.search(settings.BM_REGEX_DATE_FORMAT, weather_date):

        return Response({'detail': 'wrong date formate.'
                         ' Please Check date fromate'},
                        status=status.HTTP_400_BAD_REQUEST)
    CO_code_name = 'co'
    SO2_code_name = 'so2'
    result = {}
    status_code = status.HTTP_200_OK

    # if the hosting teams has no need for cache
    # function, then they can simple turn this
    # as `False`.
    if not settings.BM_AIRPOLLUTION_DATA_NEED_CACHE:

        CO_data = get_openweather_data(lat, lon, CO_code_name)
        SO2_data = get_openweather_data(lat, lon, SO2_code_name)

        CO_num_days = get_count_days(CO_data['time'])
        SO2_num_days = get_count_days(SO2_data['time'])

        if CO_num_days >= len(caches_content['data']):

            logger.error('Computated days should not exceed'
                         ' the max_days count. Last update date'
                         ' {}, Gas Type: {}'
                         ' '.format(caches_content['time'],
                                    CO_code_name))

            CO_data =  empty_gas_type()

        else:

            CO_data = CO_data[CO_num_days]

        if SO2_num_days >= len(caches_content['data']):


            logger.error('Computated days should not exceed'
                         ' the max_days count. Last update date'
                         ' {}, Gas Type: {}'
                         ' '.format(caches_content['time'],
                                    SO2_code_name))

            SO2_data =  empty_gas_type()

        else:

            SO2_data = SO2_data[SO2_num_days]

        result[CO_code_name] = CO_data
        result[SO2_code_name] = SO2_data[SO2_num_days]

        return Response({'detail': result},
                        status=status_code)

    CO_CACHES_NAME = 'airPollution_CO_%s_%s' % (lat, lon)
    SO2_CACHES_NAME = 'airPollution_SO2_%s_%s' % (lat, lon)

    CO_caches_content = cache.get(CO_CACHES_NAME, None)
    SO2_caches_content = cache.get(SO2_CACHES_NAME, None)


    #  checking the caches is present or not
    if not CO_caches_content:

        # setting the caches
        logger.debug('setting cache for CO gas')   
        set_caches_redis(lat, lon, CO_code_name, CO_CACHES_NAME)

    else:

        result[CO_code_name] = get_caches_redis(CO_caches_content,
                                                CO_code_name)
        logger.debug('setting the CO result')

    #  checking the caches is present or not
    if not SO2_caches_content:

        logger.debug('setting cache for SO2 gas')   
        set_caches_redis(lat, lon, SO2_code_name, SO2_CACHES_NAME)

    else:

        result[SO2_code_name] = get_caches_redis(SO2_caches_content,
                                                 SO2_code_name)
        logger.debug('setting the SO2 result')

    #  Checking the content is present on both.
    if not result.get(CO_code_name) and not result.get(SO2_code_name):

        #  this is used, that celery is async task
        #  which they may or may not return data suddenly,
        #  so we are computing after little time out.

        CO_caches_content = cache.get(CO_CACHES_NAME)
        SO2_caches_content = cache.get(SO2_CACHES_NAME)

        result[CO_code_name] = get_caches_redis(CO_caches_content,
                                                CO_code_name)

        result[SO2_code_name] = get_caches_redis(SO2_caches_content,
                                                 SO2_code_name)
    return Response({'detail': result},
                    status=status_code)
