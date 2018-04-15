from django.test import TestCase
from rest_framework.response import Response

from weather2.views import get_air_pollution
# Create your tests here.

class ViewGetAirPollution(TestCase):

    def test_result_airpollution_equal(self):
        self.assertEqual(Response, get_air_pollution(13, 80))
