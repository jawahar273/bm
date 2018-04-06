
from django.utils import timezone
from django.db import models

'''The weather models stores the information about the weather of
specificy area which given by the users. The api developed based on
Open weather map's `air pollution<http://openweathermap.org/api/pollution/co>`_
which is beta api. Remeber the api BM's weather api may changes
depones on open weather's api.
'''

GAS_TYPE_CHOICES = (
    ('CO', 'Carbon Monoxide Data'),
    ('SO2', 'Sulfur Dioxide Data'),
    # ('O3', 'Ozone Data'),
    # ('NO2', 'Nitrogen Dioxide Data')
)


class AirPollution(models.Model):

    gas_type = models.CharField(max_length=3, choices=GAS_TYPE_CHOICES)

    #  get the last time update of its content.
    last_update = models.DateTimeField()
    #  get the last timestramp update in db
    last_db_update_date = models.DateTimeField(default=timezone.now,
                                               blank=True)
    #  get the center station's location.
    location_lat = models.DecimalField(max_digits=14, decimal_places=4,
                                       default=0)
    location_lon = models.DecimalField(max_digits=15, decimal_places=4,
                                       default=0)

    class Meta:
        unique_together = (('location_lat',
                           'location_lon'), )

    def __str__(self):
        return ('Last Update-{:%Y-%m-%d %H:%M}'
                ' GasType-{}'.format(self.last_update,
                                     self.gas_type.upper()))


class AirPollutionData(models.Model):

    data_base = models.ForeignKey('AirPollution',
                                  related_name='air_pollution_data',
                                  on_delete=models.CASCADE)
    precision = models.FloatField()
    pressure = models.FloatField()
    value = models.FloatField()
    weather_date = models.DateField(null=True)

    def __str__(self):
        return ('Date-{} Base id-{:d}, Pressure-{:.2f}'
                ' Gas Type -{}'.format(self.weather_date,
                                       self.data_base.id,
                                       self.pressure,
                                       self.data_base.gas_type.upper()))
