from django.urls import include, path
from rest_framework import routers

from .views import CSVManagerViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'files', CSVManagerViewSet, basename='file_meta')

urlpatterns = [
    path('', include(router_v1.urls)),
]
