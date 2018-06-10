import datetime
import logging

from django.core.cache import cache
from django.conf import settings
from django.db.utils import IntegrityError
from django.db import transaction
import pandas as pd
import numpy as np
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from packages.models import ItemsList  # , UploadKey, UploadKeyList
from packages.config import PaymentTypeNumber
from packages.flat_file_interface.base_excel_interface import (
    BaseExcelClass,
    BaseExcelInterFaceException,
)
from packages.utils import to_percentage
from packages.config import PaymentTypeNumber

CHANNEL_LAYER = get_channel_layer()
logger = logging.getLogger(__name__)


class PandasInterfaceException(BaseExcelInterFaceException):
    pass


class PandasInterfaceNotImplement(PandasInterfaceException):
    pass


class PandasExcelAPI(BaseExcelClass):

    def __init__(self, user_id):
        """
        Using Pandas libery as working this Class is been
        working on.
        """
        super(PandasExcelAPI, self).__init__(user_id)
        self.read_flag = False  # to make read function called first
        self.dataContent = None
        self.payment_type = PaymentTypeNumber.paytm_type()
        # flag for excel type
        self.user_id = user_id
        temp = "{}.{}".format(settings.BM_NOTIFICATION_CHANNEL_NAME, user_id)
        self.channel_name = cache.get(temp)

    def read_excel(self, name, **kargs):
        """
        """

        super().read_excel(name, **kargs)
        sheet_name = kargs.get("sheet_name", 0)
        names = kargs.get("names", None)
        self.read_flag = True
        self.dataContent = pd.read_excel(name, sheet_name, names)

    def read_csv(self, name, **kargs):

        super().read_csv(name, **kargs)
        usecols = kargs.get("usecols", None)
        #  usecols=None
        self.read_flag = True
        self.dataContent = pd.read_csv(name, usecols=usecols)

    def data(self):

        return self.dataContent

    def mapping_fields(self, entry_type, options=None):

        super().mapping_fields(options)
        assert self.read_flag, "Please call read method first"
        self.payment_type = entry_type

        if entry_type == PaymentTypeNumber.paytm_type():

            self.paytm_process()

        else:

            raise PandasInterfaceNotImplement(
                "other than paytm csv " "function is not been" " implemented"
            )
        # self.dataContent.rename(options, inplace=True)

    def paytm_process(self):

        self.payment_type = 1
        # pre_drop_fileds =
        post_drop_fileds = ["Status"]
        fileds = settings.BM_PAYTM_USE_FILEDS
        #  drop unwanted columns as preprocessing.
        #  self.dataContent.drop(pre_drop_fileds, axis=1, inplace=True)
        #  drop the if the status other than `SUCCESS`.

        self.dataContent.drop(
            self.dataContent[self.dataContent.Status != "SUCCESS"].index, inplace=True
        )

        #  drop the row which has NaN in there cell of `Debit`.
        self.dataContent.drop(
            self.dataContent[pd.isna(self.dataContent.Debit)].index, inplace=True
        )

        #  droping the unwanted columns to reduce the columns after finishing
        #  the nessary steps.
        self.dataContent.drop(post_drop_fileds, axis=1, inplace=True)

        #  renaming the columns of the fileds.
        self.dataContent.rename(index=str, columns=fileds, inplace=True)
        self.dataContent.index = np.arange(0, len(self.dataContent))

        #  changing the date format.
        formater = None

        if settings.BM_PAYTM_DATE_OR_DATETIME == 0:

            formater = settings.BM_STANDARD_DATEFORMAT

        elif settings.BM_PAYTM_DATE_OR_DATETIME == 1:

            formater = settings.BM_ISO_8601_TIMESTAMP

        paytm_date_format = lambda x: datetime.datetime.strptime(
            x, settings.BM_PAYTM_DATE_FORMAT
        ).strftime(formater)
        self.dataContent["date"] = self.dataContent.date.map(paytm_date_format)

    def get_info(self):

        shape = self.dataContent.shape
        details = {"row": shape[0], "columns": shape[1]}

        return details

    def get_mem_info(self):
        """
        Only for the this class
        """

        return self.dataContent.info()

    # def pre_process_ItemList(self, data, inx):

    def insert_db(self):

        super(PandasExcelAPI, self).insert_db(self.user_id)
        user_id = self.user_id
        data = self.dataContent.to_dict("date")
        row = self.get_info()["row"]
        # temp = User.objects.get(id=user_id)

        # upload_key = UploadKeyList(user=temp)
        # upload_key.save()

        for inx in range(0, row):

            name = data["name"][inx]
            group = data["group"][inx]
            place = "online"
            amount = data["amount"][inx]
            payment_type = self.payment_type
            date = data["date"][inx]
            items = ItemsList(
                name=name,
                group=group,
                total_amount=amount,
                place=place,
                entry_type=payment_type,
                date=date,
                user_id=user_id,
            )

            try:

                with transaction.atomic():

                    items.save()

                self.as_msg_client(inx, row)

            except IntegrityError:

                self.as_msg_client(inx, row)

            # UploadKey(upload_keys=upload_key.id, content_key=items.id).save()

        logger.info("uploading has finished")
        self.dataContent = None

        self.close_connection()

    def api_name(self):

        return "Pandas Flat File Interface"

    def as_msg_client(self, current_value, total_value):

        value = to_percentage(current_value, total_value)
        async_to_sync(CHANNEL_LAYER.send)(
            self.channel_name, {"type": "upload.status", "status": str(value)}
        )

    def close_connection(self):
        async_to_sync(CHANNEL_LAYER.send)(self.channel_name, {"type": "disconnect"})
