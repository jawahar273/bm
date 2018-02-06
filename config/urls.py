from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.contrib.auth import views as auth_views

from rest_framework import routers
from allauth.account.views import confirm_email

from bm.users.views import (redirect_after_email_confirm, change_password,
                            login_after_password_change, 
                            change_password_done, 
                            display_home_page)
rest_router = routers.DefaultRouter()
# rest_router.register('package/settings', UserProfileSettingsView, base_name='packages_profile_settings')

api_url = []
if settings.DEBUG:
    from rest_framework_swagger.views import get_swagger_view
    schema_view = get_swagger_view(title='Deliver API')
    api_url += [url(r'^docs$', schema_view)]


api_url += [
    url(r'^rest-auth/password/reset/confirm/', login_after_password_change,
       name='account_change_password'),
   url(r'^package/', include('packages.urls', namespace='packages')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^accounts-rest/registration/account-confirm-email/(?P<key>[-:\w]+)/$', confirm_email, name='account_confirm_email'),
]
# api_url.extend(rest_router.urls)


urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # Your stuff: custom urls includes go here
    url(r'^api/', include(api_url)),
    url(r'verfied-success/$', redirect_after_email_confirm, name="verfied-success" ),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
       TemplateView.as_view(template_name='account/password_rest_confirm_form.html'), name="password_reset_confirm" ),
    url(r'^done', change_password_done, name='change_password_done'),
    url(r'^$', display_home_page,
           name='home',),
    # url(r'^', include('django.contrib.auth.urls')),
    # url(r'', )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
        # url(r'^$', TemplateView.as_view(template_name='pages/home.html'),
        #    name='home'),
        url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'),
           name='about'),
 
        # User management
        url(r'^accounts/', include('allauth.urls')),
        url(r'^users/', include('bm.users.urls', namespace='users')),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns


