from django.db import models
from django.core.exceptions import ValidationError

class System(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Metric(models.Model):
    system = models.ForeignKey(System, related_name='metrics', on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('system', 'name', 'timestamp')

    def __str__(self):
        return f"{self.system.name} - {self.name} @ {self.timestamp}: {self.value}"

class AlertRule(models.Model):
    system = models.ForeignKey(System, related_name='alert_rules', on_delete=models.CASCADE, default=None)
    metric_name = models.CharField(max_length=100, default='cpu_usage')
    threshold = models.FloatField()
    is_active = models.BooleanField(default=True)
    notify_email = models.EmailField(blank=True)

    def clean(self):
        # Notification validation
        if self.notify_email:
            # EmailField already validates, but you can add more checks here if needed
            if not self.notify_email or '@' not in self.notify_email:
                raise ValidationError("Notification email must be a valid email address.")
        
        # Threshold validation example: enforce a minimum value for CPU usage
        if self.metric_name == "cpu_usage" and (self.threshold < 0 or self.threshold > 100):
            raise ValidationError("CPU usage threshold must be between 0 and 100.")

        # You can add more metric-specific rules here
        # For example, memory_usage must be >= 0, etc.

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure validation is called
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Alert on {self.system.name}:{self.metric_name} if >= {self.threshold}"