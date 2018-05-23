
from bm.users.models import User
from bm.users.utils import import_class


def test_import_class(value="bm.users.models.User"):
    assert import_class(value) == User
