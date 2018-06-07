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


class PackageSettingsGeoloc:

    @staticmethod
    def interval_time():
        return 60  # equal to mins.

    @staticmethod
    def max_interval_time():
        # mins
        return 420

    @staticmethod
    def min_interval_time():
        # mintus
        return 20
