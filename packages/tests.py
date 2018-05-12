
from test_plus.test import TestCase

from packages.utils import to_hexdigit

# Create your tests here.


def test_to_hexdigit():
    assert (to_hexdigit('Budget Management') == '36fc12fd0724ea6374806883043382eb')


def test_to_percentage():
    assert  to_percentage(1423, 4560) == 31