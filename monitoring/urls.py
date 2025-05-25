from rest_framework.routers import DefaultRouter
from .views import SystemViewSet, MetricViewSet, AlertRuleViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'systems', SystemViewSet)
router.register(r'metrics', MetricViewSet)
router.register(r'alertrules', AlertRuleViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]