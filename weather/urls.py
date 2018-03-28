from django.conf import settings
from django.conf.urls import url


from weather.views import get_air_pollution


urlpatterns = [
    url('air-pollution/(?P<weather_date>{})'
        '/(?P<lat>{})/(?P<lon>{})'.format(settings.BM_REGEX_DATE_FORMAT,
                                          '[0-9]{0,3}',
                                          '[0-9]{0,3}'),
        get_air_pollution)
]
