
from django.conf.urls import url

from packages.consumers import BMNotifcationConsumer

packages_ws_urlpatterns = [url(r"^ws/upload_status/$", BMNotifcationConsumer)]
