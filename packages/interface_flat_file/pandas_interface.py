import datetime

# import os
# import sys

import pandas as pd

# sys.path.append('..')
from packages.models import ItemsList
from packages.interface_flat_file.base_excel_interface import (BaseExcelClass,
    BaseExcelInterFaceException)


class PandasExcelAPI(BaseExcelClass):

    def __init__(self):
        '''
        '''
        super(PandasExcelAPI, self).__init__()
        self.read_flag = False  # to make read function called first
        self.dataContent = None
        self.payment_type = 2  # flag for excel type

    def read_excel(self, name, sheet_name=0, names=None):
        '''
        '''
        super().read_excel(name, sheet_name, names)
        self.read_flag = True
        self.dataContent = pd.read_excel(name, sheet_name, names)

    def read_csv(self, name):
        super().read_csv(name)
        self.read_flag = True
        self.dataContent = pd.read_csv(name)

    def data(self):
        return self.dataContent

    def mapping_fields(self, options=None):
        super().mapping_fields(options)
        assert self.read_flag, 'Please call read method first'
        self.paytm_process()
        # self.dataContent.rename(options, inplace=True)

    def paytm_process(self):
        self.payment_type = 1
        pre_drop_fileds = ['Wallet Txn ID', 'Comment', 'Transaction Breakup']
        post_drop_fileds = ['Debit', 'Credit', 'Status']
        fileds = {
            'Date': 'date',
            'Activity': 'group',
            'Source/Destination': 'name',
        }
        self.dataContent.drop(pre_drop_fileds, axis=1, inplace=True)
        self.dataContent.drop(
            self.dataContent[self.dataContent.Status != 'SUCCESS'].index,
            inplace=True)
        self.dataContent['amount'] = pd.concat([
            self.dataContent.Debit.dropna(),
            self.dataContent.Credit.dropna()])
        self.dataContent.drop(post_drop_fileds, axis=1, inplace=True)
        self.dataContent.rename(index=str, columns=fileds, inplace=True)
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

    # def pre_process_ItemList(self, data, inx):

    def insert_db(self):
        # [self.pre_process_ItemList()]
        data = self.dataContent.to_dict('date')
        # for inx in range(0, self.get_info()['row']):
        #     inx = str(inx)
        #     name = data['name'][inx]
        #     group = data['group'][inx]
        #     place = 'online'
        #     amount = data['amount'][inx]
        #     payment_type = self.payment_type
        #     date = data['date'][inx]
        #     items = ItemsList(name=name, group=group,
        #             total_amount=amount, place=place,
        #             entry_type=payment_type,
        #             date=date,
        #             user_id=1)
        #     # print(items.total_amount, inx)
        #     items.save()

    def api_name(self):
        super().api_name()
        return self.__class__


class PandaExcelInterfaceException(BaseExcelInterFaceException):
    pass
