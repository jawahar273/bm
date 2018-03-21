from django.contrib import admin

# Register your models here.
from weather.models import AirPollution, AirPollutionData

admin.site.register([AirPollution, AirPollutionData])
