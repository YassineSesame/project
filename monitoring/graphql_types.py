import graphene
from graphene_django import DjangoObjectType
from .models import Metric, AlertRule

class MetricType(DjangoObjectType):
    class Meta:
        model = Metric
        fields = '__all__'

class AlertRuleType(DjangoObjectType):
    class Meta:
        model = AlertRule
        fields = '__all__'

class Query(graphene.ObjectType):
    metrics = graphene.List(MetricType)
    alert_rules = graphene.List(AlertRuleType)

    def resolve_metrics(root, info):
        return Metric.objects.all()

    def resolve_alert_rules(root, info):
        return AlertRule.objects.all()

class CreateMetric(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        value = graphene.Float(required=True)
        description = graphene.String()

    metric = graphene.Field(MetricType)

    @staticmethod
    def mutate(root, info, name, value, description=""):
        metric = Metric.objects.create(name=name, value=value, description=description)
        return CreateMetric(metric=metric)

class Mutation(graphene.ObjectType):
    create_metric = CreateMetric.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)