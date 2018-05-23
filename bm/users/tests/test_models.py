from unittest import skip

from test_plus.test import TestCase


# @skip("Don't want to test")
class TestUser(TestCase):

    def setUp(self):
        self.user = self.make_user()

    def test__str__(self):
        self.assertEqual(
            self.user.__str__(),
            "testuser",  # This is the default username for self.make_user()
        )
        print("user-id> ", self.user.id)
        # find the user id number

    # def test_get_absolute_url(self):
    #     self.assertEqual(self.user.get_absolute_url(), "/users/testuser/")
