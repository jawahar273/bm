

def flatter_list(items):
    '''
     fastest way to flatten list of elements
     Eg: [(1, 2), (2, 45)] => [1, 2, 2, 45]
    '''
    return [item for sublist in items for item in sublist]


class PaymentTypeNumber(object):
    '''
    A configuration file representaion of
    payment type 
    +------------+-------------------+
    | Payment Type Name   |  Value   |
    +============+===================+
    | Other  Payment      |    0     |
    +------------+-------------------+
    | Normal  Payment     |    1     |
    +------------+-------------------+
    | Paytm  Payment      |    2     |
    +------------+-------------------+
    '''
    # def __init__(self, arg):
    payment_type = {
        'other': 0,
        'default': 1,
        'paytm': 2,
    }

    @staticmethod
    def pay_method(value):
        value = value.lower()
        return PaymentTypeNumber.payment_type[value]
        
