
from abc import ABC, abstractmethod


class BaseExcelClass(ABC):
    '''
    Base excel class will be use as abstract class
    for making interface between the excel and csv
    file(flat file) to update into server data base
    as django model. Accept file only are excel and
    CSV along.
    .. notes::
       Try not use pandas function directly as possible
    '''

    def __init__(self, user_id):
        pass

    @abstractmethod
    def read_excel(self, name, **kargs):
        pass

    @abstractmethod
    def read_csv(self, name):
        pass

    @abstractmethod
    def data(self):
        pass

    @abstractmethod
    def mapping_fields(self, options):
        '''
        Convert Field is a function that help mapping the
        field(columns of excel)
        with :model: `packages.ItemsList`.

        @params options it is a dict() object
        '''
        pass

    @abstractmethod
    def paytm_process(self):
        pass

    @abstractmethod
    def insert_db(self):
        '''
        Inserting the value of excel into db of :model: `packages.ItemsList`.
        '''
        pass

    @abstractmethod
    def get_info(self):
        pass

    @abstractmethod
    # @classmethod
    def api_name(self):
        pass


class BaseExcelInterFaceException(Exception):
    pass
