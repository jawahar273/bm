
from test_plus.test import TestCase

from packages.utils import to_hexdigit, to_percentage


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
