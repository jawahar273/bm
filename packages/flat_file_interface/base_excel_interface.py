
from abc import ABC, abstractmethod

from django.conf import settings
from django.core.cache import cache


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
        '''Read the given file using name from in the
        server.

        :param name: [file name of the data contains]
        :type name: [str]
        '''
        pass

    @abstractmethod
    def read_csv(self, name, **kargs):
        '''Read the given file using name from in the
        server.

        :param name: [file name of the data contains]
        :type name: [str]
        '''
        pass

    @abstractmethod
    def data(self):
        '''This method return the data of the read
        part.

        '''
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
    def insert_db(self, user_id):
        '''
        Inserting the value of excel into db of :model: `packages.ItemsList`.
        '''

        if settings.DEBUG:

            print('testing abstrac method')

        if cache.get(settings.BM_CURRENT_USER_UPLOAD_NAME + user_id):
            cache.set(settings.BM_CURRENT_USER_UPLOAD_NAME + user_id,
                      user_id,
                      settings.BM_CURRENT_USER_UPLOAD_CACHE_TIMEOUT)

    @abstractmethod
    def get_info(self):
        pass

    @abstractmethod
    # @classmethod
    def api_name(self):
        pass


class BaseExcelInterFaceException(Exception):
    pass
