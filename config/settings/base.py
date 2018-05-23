"""
Base settings for bm project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import datetime

import environ

ROOT_DIR = environ.Path(__file__) - 3  # (bm/config/settings/base.py - 3 = bm/)
APPS_DIR = ROOT_DIR.path("bm")

# Load operating system environment variables and then prepare to use them
env = environ.Env()

# .env file, should load only in development environment
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)

if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables defined in the .env file,
    # that is to say variables from the .env files will only be used if not defined
    # as environment variables.
    env_file = str(ROOT_DIR.path(".env"))
    print("Loading : {}".format(env_file))
    env.read_env(env_file)
    print("The .env file has been loaded. See base.py for more information")

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    # Default Django apps:
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Useful template tags:
    # 'django.contrib.humanize',
    # Admin
    "django.contrib.admin",
]
THIRD_PARTY_APPS = [
    "channels",
    "crispy_forms",  # Form layouts
    "allauth",  # registration
    "allauth.account",  # registration
    # 'allauth.socialaccount',  # registration
    "rest_framework",  # rest framework
    "rest_framework.authtoken",  # for django-rest-auth
    "rest_auth",  # for django-rest-auth
    "rest_auth.registration",  # for django-rest-auth
    "corsheaders",  # as CORS handler for djagno rest framework
]

# Apps specific for this project go here.
LOCAL_APPS = [
    # custom users app
    "bm.users.apps.UsersConfig",
    # 'bm.taskapp.celery.CeleryConfig',
    # Your stuff: custom apps go here
    "packages",
    # 'weather',
    "weather2",
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
INSTALLED_APPS += env.list("BM_OPTIONAL_BASE_APPS", default=[])

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {"sites": "bm.contrib.sites.migrations"}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (str(APPS_DIR.path("fixtures")),)

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""jawahar""", "jawahar273@gmail.com")]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
# Uses django-environ to accept uri format
# See: https://django-environ.readthedocs.io/en/latest/#supported-types

DATABASES = {
    "default": env.db(
        "DATABASE_URL", default="postgres://jawahar:jon2speed@localhost/bm"
    )
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = "UTC"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [str(APPS_DIR.path("templates"))],
        "OPTIONS": {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            "debug": DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                # Your stuff: custom template context processors go here
            ],
        },
    }
]

# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap4"

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR("staticfiles"))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR.path("static"))]

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR("media"))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# PASSWORD STORAGE SETTINGS
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]

# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Some really nice defaults
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
ACCOUNT_ADAPTER = "bm.users.adapters.AccountAdapter"
SOCIALACCOUNT_ADAPTER = "bm.users.adapters.SocialAccountAdapter"

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "users:redirect"
LOGIN_URL = "account_login"
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "account_logout"
# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = "slugify.slugify"

# ######### CELERY
INSTALLED_APPS += ["bm.taskapp.celery.CeleryConfig"]
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="amqp://")
# db+postgres://jawahar:jon2speed@localhost/bm
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="redis://")

# if CELERY_BROKER_URL == 'django://':
#     CELERY_RESULT_BACKEND = 'redis://'
# else:
#     CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# ######### END CELERY


# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r"^admin/"

# Your common stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------

#  Django Channel config
ASGI_APPLICATION = "bm.routing.application"
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

#  Date and time format
BM_REGEX_DATE_FORMAT = r"(19|20)\d\d([- /.])(0[1-9]|1[012])\2(0[1-9]|[12][0-9]|3[01])"
BM_ISO_8601_TIMESTAMP = "%Y-%m-%dT%H:%M:%Sz"
BM_STANDARD_DATEFORMAT = "%Y-%m-%d"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        # 'rest_framework.authentication.TokenAuthentication',
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
    ),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "EXCEPTION_HANDLER": (
        "packages.serializers_childs."
        "package_rest_exceptionHandling"
        ".custom_exception_handler"
    ),
    "DEFAULT_PAGINATION_CLASS": ("rest_framework.pagination." "LimitOffsetPagination"),
    "PAGE_SIZE": 100,
}

REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "bm.users.serializer.UserSerializer"
}

JWT_AUTH = {
    "JWT_EXPIRATION_DELTA": datetime.timedelta(days=2),
    "JWT_AUTH_HEADER_PREFIX": "Token",
}

CORS_ORIGIN_ALLOW_ALL = True


SHOW_REQUEST_HEADERS = True
CORS_ALLOW_HEADERS = (
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "content-disposition",
)
# allauth setting keys
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_VERIFICATION = "optional"
# ACCOUNT_EMAIL_VERIFICATION ="mandatory"
ACCOUNT_EMAIL_MAX_LENGTH = 40
TEMPLATE_EXTENSION = "html"
CONFIRM_EMAIL_ON_GET = False
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = "verfied-success"
OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = True

# Relative to flat file setting
BM_FLAT_FILE_INTERFACE = "pandas"
BM_EXPIRY_TIME_FLAT_FILT_IN_MINS = env.int(
    "BM_EXPIRY_TIME_FLAT_FILT_IN_MINS", default=480
)
BM_PAYTM_USE_FILEDS = {
    "Date": "date",
    "Activity": "group",
    "Source/Destination": "name",
    "Debit": "amount",
}

# open weather api key
BM_OPEN_WEATHER_MAP = env("BM_OPEN_WEATHER_MAP_API", default="")

#  type of cache timeout
#  date
#  day
# @optional keys
BM_WEATHER_DATA_CACHE_TYPE = env("BM_WEATHER_DATA_CACHE_TYPE", default="day")
BM_AIRPOLLUTION_DATA_NEED_CACHE = env.bool(
    "BM_AIRPOLLUTION_DATA_NEED_CACHE", default=True
)

#  Celery network request timeout
BM_CONNECTION_TIMEOUT = env.float("BM_CONNECTION_TIMEOUT", default=5.0)

BM_READ_TIMEOUT = env.float("BM_READ_TIMEOUT", default=30.0)

# Currency system
BM_CURRENCY_DETAIL_JSON_FILE = "commmon-currency.json"

# flat file related
BM_CURRENT_USER_UPLOAD_NAME = env(
    "BM_CURRENT_USER_UPLOAD_NAME", default="current-upload-user:"
)
# #SECS
# @review
BM_CURRENT_USER_UPLOAD_CACHE_TIMEOUT = env.int(
    ("BM_CURRENT_USER_UPLOAD_CACHE" "_TIMEOUT"), default=90
)
# Message to user
BM_TO_USER_MESSAGE_WARNING = env("BM_TO_USER_MESSAGE_WARNING", default="")
