from django.conf.urls import url
from django.conf import settings

from . import views

app_name = "users"
urlpatterns = [
    # url(regex=r"^$", view=views.handling_user),
]

debuger_url = [
    url(regex=r"^list/$", view=views.UserListView.as_view(), name="list"),
    url(regex=r"^~redirect/$", view=views.UserRedirectView.as_view(), name="redirect"),
    url(
        regex=r"^(?P<username>[\w.@+-]+)/$",
        view=views.UserDetailView.as_view(),
        name="detail",
    ),
    url(regex=r"^~update/$", view=views.UserUpdateView.as_view(), name="update"),
]

if settings.DEBUG and False:
    urlpatterns += debuger_url
