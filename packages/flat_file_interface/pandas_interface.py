import datetime

# import os
# import sys

import pandas as pd
import numpy as np

# sys.path.append('..')
from packages.models import ItemsList
from packages.config import PaymentTypeNumber
from packages.flat_file_interface.base_excel_interface import (BaseExcelClass,
                                            BaseExcelInterFaceException)


class PandaInterfaceException(BaseExcelInterFaceException):
    pass


class PandasInterfaceNotImplement(PandaInterfaceException):
    pass


class PandasExcelAPI(BaseExcelClass):

    def __init__(self):
        '''
        Using Pandas libery as working this Class is been
        working on.
        '''
        super(PandasExcelAPI, self).__init__()
        self.read_flag = False  # to make read function called first
        self.dataContent = None
        self.payment_type = 2  # flag for excel type

    def read_excel(self, name, **kargs):
        '''
        '''
        super().read_excel(name, **kargs)
        sheet_name = kargs.get('sheet_name', 0)
        names = kargs.get('names', None)
        self.read_flag = True
        self.dataContent = pd.read_excel(name, sheet_name, names)

    def read_csv(self, name, **kargs):
        super().read_csv(name, **kargs)
        usecols = kargs.get('usecols', None)
        #  usecols=None
        self.read_flag = True
        self.dataContent = pd.read_csv(name, usecols=usecols)

    def data(self):
        return self.dataContent

    def mapping_fields(self, entry_type, options=None):
        super().mapping_fields(options)
        assert self.read_flag, 'Please call read method first'
        self.payment_type = entry_type
        if entry_type == PaymentTypeNumber.paytm_type()['id']:
            self.paytm_process()
        else:
            raise PandasInterfaceNotImplement('other than paytm csv '
                                              'function is not been implemented')
        # self.dataContent.rename(options, inplace=True)

    def paytm_process(self):
        self.payment_type = 1
        # pre_drop_fileds =
        post_drop_fileds = ['Status']
        fileds = {
            'Date': 'date',
            'Activity': 'group',
            'Source/Destination': 'name',
            'Debit': 'amount'
        }
        #  drop unwanted columns as preprocessing.
        #  self.dataContent.drop(pre_drop_fileds, axis=1, inplace=True)
        #  drop the if the status other than `SUCCESS`.
        self.dataContent.drop(
            self.dataContent[self.dataContent.Status != 'SUCCESS'].index,
            inplace=True)

        #  drop the row which has NaN in there cell of `Debit`.
        self.dataContent.drop(self.dataContent[
                              pd.isna(self.dataContent.Debit)].index,
                              inplace=True)

        #  droping the unwanted columns to reduce the columns after finishing
        #  the nessary steps.
        self.dataContent.drop(post_drop_fileds, axis=1, inplace=True)

        #  renaming the columns of the fileds.
        self.dataContent.rename(index=str, columns=fileds, inplace=True)
        self.dataContent.index = np.arange(0, len(self.dataContent))

        #  changing the date format.
        paytm_date_fromat = (lambda x: datetime.datetime.strptime(
            x, '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d'))
        self.dataContent['date'] = self.dataContent.date.map(paytm_date_fromat)

    def get_info(self):
        shape = self.dataContent.shape
        details = {
            'row': shape[0],
            'columns': shape[1]
        }
        return details

    def get_mem_info(self):
        '''
        Only for the this class
        '''
        return self.dataContent.info()

    # def pre_process_ItemList(self, data, inx):

    def insert_db(self, user_id):
        # [self.pre_process_ItemList()]
        data = self.dataContent.to_dict('date')
        row = self.get_info()['row']
        for inx in range(0, row):
            name = data['name'][inx]
            group = data['group'][inx]
            place = 'online'
            amount = data['amount'][inx]
            payment_type = self.payment_type
            date = data['date'][inx]
            items = ItemsList(name=name, group=group,
                              total_amount=amount, place=place,
                              entry_type=payment_type,
                              date=date, user_id=user_id)
            # print(items.total_amount, inx)
            items.save()
        self.dataContent = None

    def api_name(self):
        # super().api_name()
        return 'Pandas Flat File Interface'