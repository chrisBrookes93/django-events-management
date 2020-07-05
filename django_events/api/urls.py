from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import api_root, EventViewSet

router = DefaultRouter()
router.register('event', EventViewSet, basename='event')

urlpatterns = [
    path('', api_root, name='api-root'),
    path('', include(router.urls))
]
