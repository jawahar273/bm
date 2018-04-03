from datetime import timedelta, datetime


from django.conf import settings

from requests import get as weather_get
from requests.exceptions import RequestException

from celery.utils.log import get_task_logger


from weather.models import GAS_TYPE_CHOICES, AirPollution, AirPollutionData

from bm.taskapp.celery import app


def delete_all_airpollution(lat, lon):
    '''Delete all the previous data in the database
    under AirPollution model

    '''

    AirPollution.object.filter(location_lat=lat,
                               location_lon=lon).delete()


@app.task(bind=True)
def celery_update_air_pollution_db(self, lat, lon, delete_all):

    get_task_logger('Initializing the air pollution update task.')

    if delete_all:

        delete_all_airpollution()

    for gtype in GAS_TYPE_CHOICES:

        gtype_code = gtype[0].lower()
        get_task_logger('Getting the gast type of {}'.format(gtype_code))
        url = ('https://api.openweathermap.org/pollution'
               '/v1/{gas_type}/{lat},{lon}'
               '/current.json'
               '?appid={appid}'.format(lat=lat,
                                       lon=lon,
                                       appid=settings.BM_OPEN_WEATHER_MAP,
                                       gas_type=gtype_code))

        try:

            connect_timeout, read_timeout = 5.0, 30.0
            content = weather_get(url,
                                  timeout=(connect_timeout,
                                           read_timeout)).json()
        except RequestException as e:

            get_task_logger('Error in the'
                            ' request connection %S', str(e))

            return

        location = content['location']
        base = AirPollution(gas_type=gtype_code,
                            last_update=content['time'],
                            location_lat=location['latitude'],
                            location_lon=location['longitude'])
        base.save()

        base_date = datetime.strptime(content['time'],
                                      settings.BM_ISO_8601_TIMESTAMP)
        temp_date = base_date

        for sub_content in content['data']:

            update_date = temp_date + timedelta(days=1)
            temp_date = update_date
            update_date = update_date.strftime(settings.BM_STANDARD_DATEFORMAT)
            sub_base = AirPollutionData(precision=sub_content['precision'],
                                        pressure=sub_content['pressure'],
                                        value=sub_content['value'],
                                        weather_date=update_date,
                                        data_base=base)
            sub_base.save()

        get_task_logger('Insert into the database successfully.')


