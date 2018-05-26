from django.conf.urls import url

from weather2.views import get_air_pollution

regex_date_valid = r"[0-9\-]{10}"

app_name = "weather2"
urlpatterns = [
    url(
        r"air-pollution/(?P<weather_date>{})"
        "/(?P<lat>{})/(?P<lon>{})/$".format(
            regex_date_valid, r"[0-9]{0,3}", r"[0-9]{0,3}"
        ),
        get_air_pollution,
    )
]
