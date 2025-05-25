from rest_framework import serializers
from .models import System, Metric, AlertRule
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = '__all__'

class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = '__all__'
        read_only_fields = ['timestamp']

class AlertRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertRule
        fields = '__all__'

    def validate(self, data):
        metric_name = data.get('metric_name')
        threshold = data.get('threshold')
        notify_email = data.get('notify_email', '')

        # Example: Only allow CPU usage thresholds between 0 and 100
        if metric_name == 'cpu_usage':
            if threshold < 0 or threshold > 100:
                raise serializers.ValidationError("CPU usage threshold must be between 0 and 100.")

        # Validate notification email (if provided)
        if notify_email:
            try:
                validate_email(notify_email)
            except DjangoValidationError:
                raise serializers.ValidationError("Invalid email address for notification.")

        # You can add more custom validation for other metric types here

        return data