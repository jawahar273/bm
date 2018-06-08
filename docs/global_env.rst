
Global Environment
==================

Global environment is an important part for the any apps one way or other. These environment is classified into type.

This project uses `django cookiecutter` as its base template. Follow other setting `Cookiecutter Settings`_ to know more.

.. _Cookiecutter Settings: https://cookiecutter-django.readthedocs.io/en/latest/settings.html

Must Set Enviroment
^^^^^^^^^^^^^^^^^^^
Remeber the intercommunication between client and server must be in secure connection.

+--------------------------+--------------------------+
| Name                     | Detail desciption        |
+==========================+==========================+
| BM_CLIENT_CROSS_DOMAIN_N | Domain name of the       |
| AME                      | client site Eg: on       |
|                          | hosting in github(github |
|                          | site) it MUST set as     |
|                          | https://userName.github. |
|                          | com. [1]_                |
+--------------------------+--------------------------+
|     Open Weather Map                                |
+--------------------------+--------------------------+
| BM_OPEN_WEATHER_MAP_API  | Get api key for the      |
|                          | openweather website by   |
|                          | signup                   |
+--------------------------+--------------------------+
| BM_DB_CONN_MAX_AGE(0mins)| Setting max connection   |
|                          | timeout for DB.          |
+--------------------------+--------------------------+


Must Review Enviroment
^^^^^^^^^^^^^^^^^^^^^^
This enviroment is kind of option but if misconfig can cause lots of
headpain.

+--------------------------+--------------------------+
| Name                     | Detail desciption        |
+==========================+==========================+
|     Forgotten Password                              |
+--------------------------+--------------------------+
| BM_CLIENT_PASSWORD_RESET | Set url of               |
| _URL(reset)              | redirection in password  |
|                          | changing.                |
+--------------------------+--------------------------+
|     Open Weather Map                                |
+--------------------------+--------------------------+
| BM_WEATHER_DATA_CACHE_TY | Set these values(day,    |
| PE                       | date) which help in      |
|                          | optimization the use of  |
|                          | openweather api key      |
|                          | `Rate Limit`_. [2]_      |
+--------------------------+--------------------------+
| BM_AIRPOLLUTION_DATA_NE  | Need the cache system    |
| ED_CACHE (True)          | for the saving the       |
|                          | air pollution data [5]_. |
+--------------------------+--------------------------+
|        Celery                                       |
+--------------------------+--------------------------+
| BM_CONNECTION_TIMEOUT    | When working with celery |
| (5.0)                    | timeout must be set for  |
|                          | `requests`_ packages     |
+--------------------------+--------------------------+
| BM_READ_TIMEOUT (30.0)   | When working with celery |
|                          | read timeout must be set |
|                          | for `requests`_ packages |
+--------------------------+--------------------------+
| Uploading                                           |
+--------------------------+--------------------------+                 |
| BM_FLAT_FILE_INTERFACE   | The Flat File interface  |
| (dict: location)         | must have three value of |
|                          | class's path in dict.    |
+--------------------------+--------------------------+
| BM_EXPIRY_TIME_FLAT_FILT |  Expiry for upload flat  |
| _IN_MINS(default: 480)   |  file in the system.     |
+--------------------------+--------------------------+
| BM_PAYTM_USE_FILEDS      | List of field which      |
|                          | will be used in          |
|                          | process the flat file    |
|                          | (only paytm).            |
+--------------------------+--------------------------+
| Pdf settings                                        |
+--------------------------+--------------------------+
| BM_STANDARD_DATE_TEMPLATE| The standard date format |
|                          | to display in PDF.       |
+--------------------------+--------------------------+
| BM_PDF_TITLE             | PDF title                |
+--------------------------+--------------------------+
| BM_PDF_DESCRIPTION       | PDF description          |
+--------------------------+--------------------------+

.. _Rate Limit: https://openweathermap.org/price/
.. _requests: http://docs.python-requests.org/en/master/

Optional Environment
^^^^^^^^^^^^^^^^^^^^
The below environment adds the given django 3rd party or local apps(which is consiter as optional) to `INSTALLED_APPS`.

+-------------------------------+----------------------------+
|           Name                |     Detail desciption      |
+===============================+============================+
|    BM_OPTIONAL_BASE_APPS      | Add the given apps to base |
+-------------------------------+----------------------------+
|    BM_OPTIONAL_LOCAL_APPS     | Add the given apps to local|
+-------------------------------+----------------------------+
|    BM_OPTIONAL_TEST_APPS      | Add the given apps to test |
+-------------------------------+----------------------------+
|    BM_OPTIONAL_PRODUCTION_APPS| Add the given apps to      |
|                               | production                 |
+-------------------------------+----------------------------+
|    BM_CURRENT_USER_UPLOAD     | This is used to set cache  |
|    _CACHE_TIMEOUT(default 90) | time out(in seconds)       |
+-------------------------------+----------------------------+

.. [1] For now, only one domain is allowed to set.
.. [2] In case many user it would be wise to set `date`. That is cache expires should be based on calucate date.
.. [3] `BM_FLAT_FILE_INTERFACE_CLASS`
.. [4] All the class's name(title case) under `xXx_interface.py` must start with the prefix of the file's name as `xXx` and that value must be given as the value for the `FLAT_FILE_INTERFACE`.
.. [5] If the cahce is set for `FALSE` then on each the client request weather data then it fech for the open weather (air pollution[beta]).