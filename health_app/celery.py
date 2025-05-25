import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "health_app.settings")

app = Celery("health_app")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


CELERY_BEAT_SCHEDULE = {
    "scrape-prometheus-every-5min": {
        "task": "monitoring.tasks.scrape_prometheus_metrics",
        "schedule": crontab(minute="*/5"),
    },
}