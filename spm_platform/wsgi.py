"""
WSGI config for spm_platform project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'apps'))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spm_platform.settings')

application = get_wsgi_application()
