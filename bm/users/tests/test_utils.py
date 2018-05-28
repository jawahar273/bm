from test_plus.test import TestCase

from bm.users.models import User
from bm.users.utils import import_class


class TestUserURLs(TestCase):

    def test_import_class(self, value="bm.users.models.User"):
        self.assertEqual(import_class(value), User)
