import datetime

from django.conf import settings
from test_plus.test import TestCase

from weather2.views import get_air_pollution
# Create your tests here.


class TestAirPollution(TestCase):

    def test_result_airpollution_equal(self):
        todays_date = datetime.datetime.strftime(datetime.datetime.now(),
                                                 settings.BM_STANDARD_DATEFORMAT)

        response = self.get(get_air_pollution(todays_date, 13, 80))
        self.assertIsInstance(response, dict)
