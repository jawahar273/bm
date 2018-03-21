import datetime


from django.conf import settings

from requests import get as weather_get

from celery.utils.log import get_task_logger


from weather.models import GAS_TYPE_CHOICES, AirPollution, AirPollutionData

from bm.taskapp.celery import app


@app.task(bind=True)
def celery_update_air_pollution_db(self, lat, lon):

    get_task_logger('Initializing the air pollution update task.')

    for gtype in GAS_TYPE_CHOICES:

        gtype_code = gtype[0].lower()
        get_task_logger('Getting the gast type of {}'.format())
        url = ('http://api.openweathermap.org/pollution'
               '/v1/{gas_type}/{lat},{lon}'
               '/current.json'
               '?appid={appid}'.format(lat=lat,
                                       lon=lon,
                                       appid=settings.OPEN_WEATHER_MAP,
                                       gas_type=gtype_code))
        content = weather_get(url).json()
        base = AirPollution(gas_type=gtype_code,
                            last_update=content['time'],
                            location_lat=content['location'],
                            location_lon=content['longitude'])
        base.save()
        base_date = datetime.datetime.strptime(content['time'],
                                               settings.ISO_8601_TIMESTAMP)

        for sub_content in content['data']:

            update_date = base_date + datetime.timedelta(days=1)
            update_date = datetime.datetime.strptime(update_date,
                                                     settings.BM_STANDARD_DATEFORMAT)

            sub_base = AirPollutionData(precision=sub_content['precision'],
                                        pressure=sub_content['pressure'],
                                        value=sub_content['value'],
                                        weather_date=update_date)
            sub_base.save()

        get_task_logger('Insert into the database successfully.')

        return True

