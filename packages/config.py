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
    settings = {"default": {"id": 0}, "paytm": {"id": 1}, "excel": {"id": 2}}

    @staticmethod
    def default_type():
        return PaymentTypeNumber.settings["default"]

    @staticmethod
    def paytm_type():
        return PaymentTypeNumber.settings["paytm"]

    @staticmethod
    def excel_type():
        return PaymentTypeNumber.settings["excel"]


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
