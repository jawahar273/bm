from django.conf import settings

__APIClass = None
__APIException = None
__APIExceptionNotImplemented = None

# rework based on importlib
if settings.FLAT_FILE_INTERFACE == 'pandas':
    from packages.flat_file_interface.pandas_interface import (PandasExcelAPI,
                                                               PandasInterfaceException,
                                                               PandasInterfaceNotImplement)

    __APIClass = PandasExcelAPI
    __APIException = PandaInterfaceException
    __APIExceptionNotImplemented = PandasInterfaceNotImplement
# in plan for future alternative class.


class FlatFileInterFaceAPI(__APIClass):
    """docstring for FlatFileInterFaceAPI"""

    def __init__(self):
        super(FlatFileInterFaceAPI, self).__init__()

    def read_file(self, file_format, name, **kargs):

        if file_format == 'csv':
            self.read_csv(name, **kargs)
        else:
            self.read_excel(name, **kargs)


class FlatFileInterFaceException(__APIException):
    pass


class FlatFileInterFaceNotImplemented(__APIExceptionNotImplemented):
    pass
