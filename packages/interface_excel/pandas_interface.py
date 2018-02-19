
import pandas as pd

from packages.interface_excel.base_excel_interface import BaseExcelClass


class PandasExcelAPI(BaseExcelClass):
    """docstring for PandasExcelAPI"""

    def __init__(self):
        super(PandasExcelAPI, self).__init__()
        self.convert_filed_flag = False

    def read_excel(self, name, sheet_name=0, names=None):
        '''

        '''
        assert self.convert_filed_flag, ('first call the '
                                '`convert_field_to_excel_field()` function.')
        super().read_excel()
        return pd.read_excel(name, sheet_name, names)

    def convert_field_to_excel_field field(self, options):
        super().convert_field_to_excel_field()

    @classmethod
    def api_name(cls):
        super().api_name()
        return cls.__name__

