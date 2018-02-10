# to class some setting for the package app


class PacConDynFields:
    '''
    Due large name nessary this class name is reduce from `PackageConfigDynamicFilds`.
    The fileds are design in key as it name and value as its default values
    which is directly send as json fields.
    '''
    settings = {
      'default': {'id': 0},
      'paytm': {'id': 1}
    }

    @staticmethod
    def dict_json():
       return PacConDynFields.settings