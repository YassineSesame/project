from django.contrib import admin
from .models import Metric, AlertRule, System

@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ("name", "value", "timestamp")
    search_fields = ("name",)

@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = ("system", "metric_name", "threshold", "notify_email", "is_active")
    search_fields = ("metric_name", "notify_email")

@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)