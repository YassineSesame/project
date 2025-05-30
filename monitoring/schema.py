import graphene
from graphene_django import DjangoObjectType
from .models import System, Metric, AlertRule

class SystemType(DjangoObjectType):
    class Meta:
        model = System
        fields = "__all__"

class MetricType(DjangoObjectType):
    class Meta:
        model = Metric
        fields = "__all__"

class AlertRuleType(DjangoObjectType):
    class Meta:
        model = AlertRule
        fields = "__all__"

class Query(graphene.ObjectType):
    all_systems = graphene.List(SystemType)
    all_metrics = graphene.List(MetricType)
    all_alert_rules = graphene.List(AlertRuleType)

    system = graphene.Field(SystemType, id=graphene.Int(required=True))
    metric = graphene.Field(MetricType, id=graphene.Int(required=True))
    alert_rule = graphene.Field(AlertRuleType, id=graphene.Int(required=True))

    def resolve_all_systems(root, info):
        return System.objects.all()

    def resolve_all_metrics(root, info):
        return Metric.objects.all()

    def resolve_all_alert_rules(root, info):
        return AlertRule.objects.all()

    def resolve_system(root, info, id):
        return System.objects.get(pk=id)

    def resolve_metric(root, info, id):
        return Metric.objects.get(pk=id)

    def resolve_alert_rule(root, info, id):
        return AlertRule.objects.get(pk=id)
    
    def resolve_latest_metrics(self, info, system_id=None, limit=10):
        qs = Metric.objects.all().order_by('-timestamp')
        if system_id:
            qs = qs.filter(system_id=system_id)
        return qs[:limit]

    def resolve_active_alert_rules(self, info, system_id=None):
        qs = AlertRule.objects.filter(is_active=True)
        if system_id:
            qs = qs.filter(system_id=system_id)
        return qs


schema = graphene.Schema(query=Query)