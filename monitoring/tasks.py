from celery import shared_task
import requests
from .models import Metric
from django.utils import timezone
import numpy as np

PROMETHEUS_URL = "http://localhost:9090/api/v1/query?query=up"

@shared_task
def scrape_prometheus_and_push():
    response = requests.get(PROMETHEUS_URL)
    data = response.json()["data"]["result"]
    for item in data:
        name = item["metric"].get("__name__", "unknown_metric")
        value = float(item["value"][1])
        Metric.objects.create(name=name, value=value, timestamp=timezone.now())

@shared_task
def anomaly_detection_task():
    # Example: find anomalies using Z-score on last 50 values for each metric
    for name in Metric.objects.values_list('name', flat=True).distinct():
        values = list(Metric.objects.filter(name=name).order_by('-timestamp').values_list('value', flat=True)[:50])
        if len(values) < 10:
            continue
        mean = np.mean(values)
        std = np.std(values)
        latest = values[0]
        z_score = (latest - mean) / std if std else 0
        if abs(z_score) > 3:  # Anomaly threshold
            print(f"Anomaly detected in {name}: value={latest} (z-score={z_score:.2f})")


@shared_task
def scrape_prometheus_metrics():
    # Example: Query CPU usage for all systems
    queries = {
        "cpu_usage": '100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)',
        "memory_usage": 'node_memory_Active_bytes',
    }
    for metric_name, prom_query in queries.items():
        response = requests.get(PROMETHEUS_URL, params={"query": prom_query})
        data = response.json()
        if data.get("status") != "success":
            continue
        for result in data["data"]["result"]:
            instance = result["metric"].get("instance", "unknown")
            value = float(result["value"][1])
            # Get or create the system
            system, _ = System.objects.get_or_create(name=instance)
            # Save metric
            Metric.objects.create(system=system, name=metric_name, value=value, timestamp=timezone.now())