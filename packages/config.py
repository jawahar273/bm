# to class some setting for the package app


class PaymentTypeNumber:
    '''
    +------------+-------------------+
    | Payment Type Name   |  Value   |
    +============+===================+
    | default Payment     |    0     |
    +------------+-------------------+
    | Paytm  Payment      |    1     |
    +------------+-------------------+
    '''
    settings = {
      'default': {'id': 0},
      'paytm': {'id': 1},
      'excel': {'id': 2},
    }

    @staticmethod
    def paytm_type():
        return PaymentTypeNumber.settings
