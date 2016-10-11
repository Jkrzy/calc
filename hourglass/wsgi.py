"""
WSGI config for hourglass project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
import newrelic.agent
from hourglass.settings_utils import load_cups_from_vcap_services

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hourglass.settings")

# Load user-provided service credentials into the environment so that
# they are available for use here, before the app is loaded
load_cups_from_vcap_services()


nr_license = os.environ.get('NEW_RELIC_LICENSE_KEY')
nr_app_name = os.environ.get('NEW_RELIC_APP_NAME')
if nr_license and nr_app_name:
    nr_settings = newrelic.agent.global_settings()
    nr_settings.license_key = nr_license
    nr_settings.app_name = nr_app_name
    newrelic.agent.initialize()

try:
    application = get_wsgi_application()
except Exception as e:
    print(e)
