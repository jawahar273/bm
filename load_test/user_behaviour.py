import logging

from locust import TaskSet, task

logger = logging.getLogger(__name__)


class UserBehavior(TaskSet):
    """This class inheried from the `TaskSet`
    to run the a specific task in hand.
    
    -- ChangeLog:
        Sunday 27 May 2018 08:10:32 AM IST
        @jawahar273 [Version 0.1]
        -1- Init Code
    """

    def __init__(self, parent):
        super().__init__(parent=parent)

        self.token_key = "Token "

    def base_url(self):
        """This method will be use the return
        the base url in the server
        
    -- ChangeLog:
        Sunday 27 May 2018 08:11:43 AM IST
        @jawahar273 [Version 0.1]
        -1- Init Code
        """
        return "/api/"

    def packages_url(self):
        """This method will be use the return
        url related to the package app.
        
    -- ChangeLog:
        Sunday 27 May 2018 08:12:22 AM IST
        @jawahar273 [Version 0.1]
        -1- Init Code
        """
        return self.base_url() + "package/"

    def user_details(self):
        """This method will be use the return
        the load testing username and password.
        
    -- ChangeLog:
        Sunday 27 May 2018 08:12:57 AM IST
        @jawahar273 [Version 0.1]
        -1- Init Code
        """
        return {"username": "demo", "password": "demobmmb"}

    def on_start(self):
        """ on_start is called
            when a Locust start before
            any task is scheduled

            -- ChangeLog:
                Sunday 27 May 2018 08:13:28 AM IST
                @jawahar273 [Version 0.1]
                -1- Init Code
        """
        self.login()

    def login(self):
        """This method running after the `on_start`

            -- ChangeLog:
                Sunday 27 May 2018 08:14:15 AM IST
                @jawahar273 [Version 0.1]
                -1- Init Code
        """

        logger.info("login user")
        response = self.client.post(
            self.base_url() + "rest-auth/login/", data=self.user_details()
        )
        self.token_key = self.token_key + response.text

        logger.debug("response from host" + str(response))
        print("Response status code:", response.status_code)
        print("Response content:", response.text)

    @task(1)
    def currency_details(self):
        """This method will call the currency details
        api and return the response status code.

        -- ChangeLog:
            Sunday 27 May 2018 08:14:39 AM IST
            @jawahar273 [Version 0.1]
            -1- Init Code
        """
        currency = self.client.get(
            self.packages_url() + "currency/",
            headers={"authentication": self.token_key},
        )

        if currency.status_code >= 300:

            logger.debug("response from host for currency {}".format(currency.text))

        else:

            logger.info("success in currency: {}".format(currency.status_code))
