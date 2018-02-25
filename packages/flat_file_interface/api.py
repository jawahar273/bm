from django.conf import settings

__APIClass = None
__APIException = None
if settings.FLAT_FILE_INTERFACE == 'pandas':
    from packages.flat_file_interface.pandas_interface import (PandasExcelAPI,
                                                               PandaExcelInterfaceException)
    __APIClass = PandasExcelAPI
    __APIException = PandaExcelInterfaceException
# in plan for future alternative class.


class FlatFileInterFaceAPI(__APIClass):
    """docstring for FlatFileInterFaceAPI"""
    def __init__(self, user_id):
        super(FlatFileInterFaceAPI, self).__init__(user_id)

    def read_file(self, file_format, **kargs):
        name = kargs.get('name')
        if file_format == 'csv':
            self.read_csv(name)
        else:
            sheet_name = kargs.get('sheet_name', 0)
            names = kargs.get('names', None)
            self.read_excel(name, sheet_name, names)


class FlatFileInterFaceException(__APIException):
    pass
