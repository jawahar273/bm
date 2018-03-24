from django.apps import AppConfig


class WeatherConfig(AppConfig):
    name = 'weather'

    def ready(self):

        from weather.receivers import get_weather_user_logged_in
