"""
Local settings for bm project.

- Run in Debug mode

- Use mailhog for emails

- Add Django Debug Toolbar
- Add django-extensions as app
"""

from .base import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG", default=True)
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env(
    "DJANGO_SECRET_KEY", default="|.`.X2i[&kdmWc|W,I^yFJ!e6sx2w]}E-*-{^qgO9&Gw~i~dWc"
)

# Mail settings
# ------------------------------------------------------------------------------

EMAIL_PORT = 1025

EMAIL_HOST = "localhost"


# CACHING
# ------------------------------------------------------------------------------
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
#         "LOCATION": "",
#     }
# }


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PICKLE_VERSION": -1,
        },
    }
}

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # "silk.middleware.SilkyMiddleware",
]
INSTALLED_APPS += ["debug_toolbar", "rest_framework_swagger", "silk"]

INTERNAL_IPS = ["127.0.0.1", "10.0.2.2", "0.0.0.0"]

DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["django_extensions"]

INSTALLED_APPS += env.list("BM_OPTIONAL_LOCAL_APPS", default=[])

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = "django.test.runner.DiscoverRunner"

########## CELERY
# In development, all tasks will be executed locally by blocking until the task returns
CELERY_ALWAYS_EAGER = True
########## END CELERY

# Your local stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
if DEBUG:
    EMAIL_HOST = "127.0.0.1"
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""
    EMAIL_PORT = 1025
    EMAIL_USE_TLS = False

# permission related issue
# from django.conf import settings
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "api_key": {"type": "apiKey", "in": "header", "name": "Authorization"}
    },
    "DOC_EXPANSION": None,
    "APIS_SORTER": None,
    "OPERATIONS_SORTER": None,
    "JSON_EDITOR": True,
    "SHOW_REQUEST_HEADERS": False,
    "SUPPORTED_SUBMIT_METHODS": ["get", "post", "put", "delete", "patch"],
    "VALIDATOR_URL": "https://online.swagger.io/validator",
}

CORS_ORIGIN_WHITELIST = ("127.0.0.1", "localhost:4300")

# remove this one

DEFAULT_FROM_EMAIL = env("DJANGO_DEFAULT_FROM_EMAIL", default="bm <noreply@localhost>")

EMAIL_SUBJECT_PREFIX = env("DJANGO_EMAIL_SUBJECT_PREFIX", default="[bm]")

SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)


# EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'

# must have protocol and end slash
CLIENT_REDIRECT_DOMAIN = "http://localhost:4300"
CLIENT_REDIRECT_URL = "reset"

CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_ALWAYS_EAGER = True

#  Django Channel config local
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("localhost", 6379)]},
        # "ROUTING": "packages.routing.packages_ws_urlpatterns"
    }
}

SWAGGER_DOCS = env.bool("BM_SWAGGER_DOCS", default=True)
