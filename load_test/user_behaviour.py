import logging

from locust import TaskSet, task

logger = logging.getLogger(__name__)


class UserBehavior(TaskSet):

    def __init__(self, parent):
        super().__init__(parent=parent)

        self.token_key = "Token "

    def base_url(self):

        return "/api/"

    def packages_url(self):

        return self.base_url() + "package/"

    def user_details(self):

        return {"username": "demo", "password": "demobmmb"}

    def on_start(self):
        """ on_start is called
            when a Locust start before
            any task is scheduled
        """
        self.login()

    def login(self):
        # self.token_key = 'Token '
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
        currency = self.client.get(
            self.packages_url() + "currency/",
            headers={"authentication": self.token_key},
        )

        if currency.status_code >= 300:

            logger.debug("response from host for currency" + currency.text)

        else:

            logger.info("success in currency", currency.status_code)
