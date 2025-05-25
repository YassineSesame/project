from django.test import TestCase
from .models import Metric, AlertRule

class MetricModelTest(TestCase):
    def test_metric_creation(self):
        m = Metric.objects.create(name="cpu", value=0.5)
        self.assertEqual(str(m), f"cpu: 0.5 at {m.timestamp}")

class AlertRuleModelTest(TestCase):
    def test_alert_rule_creation_and_validation(self):
        m = Metric.objects.create(name="memory", value=0.8)
        ar = AlertRule(metric=m, threshold=0.9, notify_via="email")
        ar.clean()  # Should not raise