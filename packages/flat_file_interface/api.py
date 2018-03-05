from django.conf import settings

__APIClass = None
__APIException = None
__APIExceptionNotImplemented = None

if settings.FLAT_FILE_INTERFACE == 'pandas':
    from packages.flat_file_interface.pandas_interface import (PandasExcelAPI,
                                                               PandaInterfaceException,
                                                               PandasInterfaceNotImplement)

    __APIClass = PandasExcelAPI
    __APIException = PandaInterfaceException
    __APIExceptionNotImplemented = PandasInterfaceNotImplement
# in plan for future alternative class.


class FlatFileInterFaceAPI(__APIClass):
    """docstring for FlatFileInterFaceAPI"""

    def __init__(self, user_id):
        super(FlatFileInterFaceAPI, self).__init__(user_id)

    def read_file(self, file_format, **kargs):
        name = kargs.get('name')

        if file_format == 'csv':
            # usecols = kargs.get('usecols', None)
            self.read_csv(name, kargs)
        else:
            # sheet_name = kargs.get('sheet_name', 0)
            # names = kargs.get('names', None)
            self.read_excel(name, kargs)


class FlatFileInterFaceException(__APIException):
    pass


class FlatFileInterFaceNotImplemented(__APIExceptionNotImplemented):
    pass
