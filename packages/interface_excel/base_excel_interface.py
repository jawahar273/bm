
from abc import ABC, abstractmethod


class BaseExcelClass(ABC):
    '''docstring for BaseExcelClass'''

    @abstractmethod
    def read_excel(self, name, sheet_name=0, names=None):
        pass

    @abstractmethod
    def convert_field_to_excel(self, options):
        '''
        Convert Field is a function that help mapping the
        field(columns of excel)
        with :model: `packages.ItemsList`.
        '''
        pass

    @abstractmethod
    def to_insert_db(self):
        '''
        Inserting the value of excel into db of :model: `packages.ItemsList`.
        '''
        pass

    @abstractmethod
    def api_name(self):
        pass



