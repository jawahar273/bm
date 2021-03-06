from django.conf import settings
from rest_framework import status
from requests import get as weather_get
from requests.exceptions import RequestException
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

#  This order is constant form.
GAS_TYPE_CHOICES = (
    ("co", "Carbon Monoxide Data"),
    ("so2", "Sulfur Dioxide Data"),
    # ('o3', 'Ozone Data'),
    # ('no2', 'Nitrogen Dioxide Data')
)


def get_air_pollution_data(lat, lon, gtype_code):
    """Using(which is general form) the function
    the weather data can be fetched
    from the openweather api(air-pollution [under beta]).

    :param lat: latitute of the user's.
    :param lon:  lontitute of the user's.
    :param gtype_code: the gas type of air pollution.
    :return: return the dict with the status code and msg/data(or both).

    ChangeLog:
    -- Wednesday 11 April 2018 10:45:58 PM IST
        @jawahar273 [Version 0.1]
        -1- Init struture of the code.
    -- Friday 13 April 2018 11:41:36 PM IST
        @jawahar273[Version 0.2]
        -1- Update in docstring.

    """

    logger.info("#[utils weather]Initializing the air pollution update task.")

    gtype_code = gtype_code.lower()
    logger.info("#[utils weather] Getting the gas type of {}".format(gtype_code))
    url = (
        "https://api.openweathermap.org/pollution"
        "/v1/{gas_type}/{lat},{lon}"
        "/current.json"
        "?appid={appid}".format(
            lat=lat, lon=lon, appid=settings.BM_OPEN_WEATHER_MAP, gas_type=gtype_code
        )
    )

    try:

        # Read the data from the server.
        connect_timeout = settings.BM_CONNECTION_TIMEOUT
        read_timeout = settings.BM_READ_TIMEOUT

        content_data = weather_get(url, timeout=(connect_timeout, read_timeout))

        success_code = status.HTTP_200_OK
        status_code = content_data.status_code

        if status_code != success_code:
            logger.fatal(
                "#[utils weather]Error from openweathermap:"
                "status code %d and the "
                "message %s " % (status_code, content_data.reason)
            )

            return {
                "msg": "something went wrong openweathermap.",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }

        content_data = content_data.json()

        # status_code = content_data.get('cod', None)

        # if status_code != success_code:

        #     logger.fatal('#[utils weather]something went wrong in the'
        #                  ' request %d and the message:'
        #                  ' %s ' % (status_code, content_data.get('message')))

        #     return {
        #            'msg': 'something went wrong.',
        #            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
        #     }
        # ----- code for the today's date value.
        return {"content_data": content_data, "code": success_code}

    except RequestException as e:

        logger.error("#[utils weather]Error in the request connection %s", str(e))

        return {
            "msg": "something went wrong.",
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        }


def empty_gas_type():
    return {"precision": 0, "pressure": 0, "value": 0, "is_empty": True}
