from locust import HttpLocust

from load_test.user_behaviour import UserBehavior


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
