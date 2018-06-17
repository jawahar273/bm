from django.conf import settings

from bm.users.utils import import_class

# rework based on importlib

_class_path = settings.BM_FLAT_FILE_INTERFACE
APIClass = import_class(_class_path["api_class"])
APIException = import_class(_class_path["api_exception"])
APIExceptionNotImplemented = import_class(_class_path["api_not_implemented"])
# in plan for future alternative class.


class FlatFileInterFaceAPI(APIClass):
    """docstring for FlatFileInterFaceAPI"""

    def __init__(self, user_id):
        super(FlatFileInterFaceAPI, self).__init__(user_id)

    def read_file(self, file_format, name, **kargs):

        if file_format == "csv":

            self.read_csv(name, **kargs)

        elif file_format == "xslx":

            self.read_excel(name, **kargs)


class FlatFileInterFaceException(APIException):
    pass


class FlatFileInterFaceNotImplemented(APIExceptionNotImplemented):
    pass
