from django.conf import settings

__APIClass = None
if settings.FLAT_FILE_INTERFACE == 'pandas':
    from pandas_interface import PandasExcelAPI
    __APIClass = PandasExcelAPI
# in plan for future alternative class.


class FlatFileInterFaceAPI(__APIClass):
    """docstring for FlatFileInterFaceAPI"""
    def __init__(self, user_id):
        super(FlatFileInterFaceAPI, self).__init__(user_id)
