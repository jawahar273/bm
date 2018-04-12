# from datetime import timedelta, datetime

from celery.utils.log import get_task_logger
# from rest_framework.response import Response
# from rest_framework import status

from bm.taskapp.celery import app
from weather2.utils import get_air_pollution_data, GAS_TYPE_CHOICES

logger = get_task_logger(__name__)


@app.task(bind=True)
def celery_get_co_data(self, lat, lon):
    '''get the value of the Carbon Monoxied
    openweather (airpollution [beta api])

    :param lat: latitute of the user's.
    :param lon:  lontitute of the user's.
    :return: Response object from django restframework

    ChangeLog:
        -- Thursday 12 April 2018 08:43:56 AM IST
            @jawahar273 [Version 0.1]
                1) Init the structure of the code.
    '''
    logger.info('#[task weather]getting the data for `CO` gas type.')

    gtype = GAS_TYPE_CHOICES[0][0].lower()
    return get_air_pollution_data(lat, lon, gtype)


@app.task(bind=True)
def celery_get_so2_data(self, lat, lon):
    '''get the value of the Carbon Monoxied
    openweather (airpollution [beta api])

    :param lat: latitute of the user's.
    :param lon:  lontitute of the user's.
    :return: Response object from django restframework


    ChangeLog:
        -- Thursday 12 April 2018 08:43:56 AM IST
            @jawahar273 [Version 0.1]
            -1- Init the structure of the code.
    '''

    logger.info('#[task weather]getting the data for `SO2` gas type.')

    gtype = GAS_TYPE_CHOICES[1][0].lower()
    return get_air_pollution_data(lat, lon, gtype)