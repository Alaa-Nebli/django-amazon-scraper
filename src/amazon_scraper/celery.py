import os

from django.conf import settings

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amazon_scraper.settings')

app = Celery('amazon_scraper')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

