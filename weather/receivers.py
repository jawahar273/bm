import logging


from django.dispatch import receiver

from allauth.account.signals import user_logged_in


from weather.tasks import celery_update_air_pollution_db as cuapd


# Get an instance of a logger
logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def get_weather_user_logged_in(sender, **kwagrs):
    '''Get the location from the user using web socket and calling
    :meth: `weather.tasks.celery_update_air_pollution_db` get the
    weather data from the service.

    :param sender: param from the `receiver` function.
    :param dict kwagrs: dict of arguments.
    '''
    logger.log(cuapd.delay(12, 77).task_id,
               'get the weather data from the service')
