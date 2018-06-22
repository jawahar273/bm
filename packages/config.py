PAYMENTTYPE = {"default": 0, "paytm": 1, "excel": 2}


# to class some setting for the package app
class PaymentTypeNumber:
    """
    +------------+-------------------+
    | Payment Type Name   |  Value   |
    +============+===================+
    | default Payment     |    0     |
    +------------+-------------------+
    | Paytm  Payment      |    1     |
    +------------+-------------------+
    """

    @staticmethod
    def default_type():
        return PAYMENTTYPE["default"]

    @staticmethod
    def paytm_type():
        return PAYMENTTYPE["paytm"]

    @staticmethod
    def excel_type():
        return PAYMENTTYPE["excel"]
