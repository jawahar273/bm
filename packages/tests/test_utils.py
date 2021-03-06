
from test_plus.test import TestCase

from packages.utils import (
    to_hexdigit,
    to_percentage,
    validate_less_than_today,
    find_dict_value,
)


# Create your tests here.
class TestPackagesUtils(TestCase):

    def test_to_hexdigit(self):
        print("test")
        self.assertEqual(
            to_hexdigit("Budget Management"), "36fc12fd0724ea6374806883043382eb"
        )

    def test_to_percentage(self):
        self.assertEqual(to_percentage(1423, 4560), 31)

        def test__str__(self):
            print("done in testing packages utils")

    def test_todays(self):
        value = validate_less_than_today("2018-05-01")
        self.assertTrue(value)
        value = validate_less_than_today("2020-05-01")
        self.assertFalse(vale)

    def test_find_dict_value(self):
        testing = {"test-1": 1, "test-2": 2, "test-3": 3}
        value = find_dict_value(3, testing)

        self.assertEqual(value, "test-3")
