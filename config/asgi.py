"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import sys

import django
from channels.routing import get_default_application

django.setup()
# application = get_default_application()


# This allows easy placement of apps within the interior
# bm directory.
app_path = os.path.dirname(os.path.abspath(__file__)).replace("/config", "")
sys.path.append(os.path.join(app_path, "bm"))

# senty can not be use as it is design for WSGI
# not to be compantable with ASGI.
if os.environ.get("DJANGO_SETTINGS_MODULE") == "config.settings.production":
    from raven.contrib.django.raven_compat.middleware.wsgi import Sentry

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.production"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
application = get_default_application()
# if os.environ.get('DJANGO_SETTINGS_MODULE') == 'config.settings.production':
#     application = Sentry(application)
# Apply ASGI middleware here.
