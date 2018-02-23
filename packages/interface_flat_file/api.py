
from pandas_interface import PandasExcelAPI

if __name__ == '__main__':

    api = PandasExcelAPI()

    api.read_csv('Paytm_Wallet_Txn_History_Csv_Feb2018_8973744171.csv')
    # print(api.dataContent)
    # print(api)
    api.mapping_fields(324)
    print(api.insert_db())
    print(api.get_info())
    print(api.api_name())
