# to class some setting for the package app

import json

class PacConDynFields:
    '''
    Due large name nessary this class name is reduce from `PackageConfigDynamicFilds`.
    The fileds are design in key as it name and value as its default values
    which is directly send as json fields.
    '''
    settings = {
      'active_paytm': 'N' # 'Y' or 'N' only
    }

    @staticmethod
    def dict_json():
       return json.dumps(PacConDynFields.settings)