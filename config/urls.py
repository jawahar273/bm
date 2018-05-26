from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

# from django.contrib.auth import views as auth_views

from rest_framework import routers

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

# from allauth.account.views import confirm_email as allauthemailconfirmation

from bm.users.views import (
    display_home_page,
    redirect_after_email_confirm,
    redirect_password_rest_done,
    handling_mail_confirm,
)

rest_router = routers.DefaultRouter()

api_url = []
if settings.DEBUG:
    from rest_framework_swagger.views import get_swagger_view

    schema_view = get_swagger_view(title="Deliver API")
    api_url += [url(r"^docs$", schema_view), url(r"^silk/", include("silk.urls"))]

handler500 = "rest_framework.exceptions.server_error"
handler400 = "rest_framework.exceptions.bad_request"

api_url += [
    url(r"^rest-auth/", include("rest_auth.urls")),
    url(r"^rest-auth/registration/", include("rest_auth.registration.urls")),
    #  url(r'^auth-jwt/', obtain_jwt_token),
    #  by replacing the with `rest-auth/login/` to obtain jwt
    #  token and making process painless.
    url(r"^rest-auth/login-auth/$", obtain_jwt_token),
    url(r"^rest-auth/login-refresh/$", refresh_jwt_token),
    url(r"^rest-auth/login-verify/$", verify_jwt_token),
    url(r"^package/", include("packages.urls")),
    # url(r'^weather/', include('weather.urls', namespace='weather')),
    url(r"^weather/", include("weather2.urls")),
]


urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),
    # Your stuff: custom urls includes go here
    url(r"^api/", include(api_url)),
    url(r"verfied-success/$", redirect_after_email_confirm, name="verfied-success"),
    url(
        r"^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        redirect_password_rest_done,
        name="password_reset_confirm",
    ),
    url(
        r"^accounts/confirm-email/(?P<key>[-:\w]+)/$",
        handling_mail_confirm,
        name="redirect_on_mail_confirm",
    ),
    url(r"^$", display_home_page, name="home"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    """
    This allows the error pages to be debugged during development, just visit
    these url in browser to see how these error pages look like.
    """
    urlpatterns += [
        url(
            r"^400/$",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        url(
            r"^403/$",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        url(
            r"^404/$",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        url(r"^500/$", default_views.server_error),
        url(
            r"^about/$",
            TemplateView.as_view(template_name="pages/about.html"),
            name="about",
        ),
        # User management
        url(r"^accounts/", include("allauth.urls")),
        url(r"^users/", include("bm.users.urls")),
    ]

    if "debug_toolbar" in settings.INSTALLED_APPS:

        import debug_toolbar

        urlpatterns = [url(r"^__debug__/", include(debug_toolbar.urls))] + urlpatterns
