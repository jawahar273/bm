from test_plus.test import TestCase

from packages.models import UploadKeyList, UploadKey


class TestUploadKeys(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.upload_key_list = UploadKeyList(user_id=1)
        cls.upload_key_list.save()

        cls.upload_key = UploadKey(upload_keys=cls.upload_key_list.id, content_key=1)
        cls.upload_key.save()

        def test__str__(self):
            print("done in testing upload keys")
