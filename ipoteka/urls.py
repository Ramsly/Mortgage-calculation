from django.urls import path, include
from rest_framework import routers

from .views import IpotekaModelViewSet

routers = routers.DefaultRouter()

routers.register(r'offer', IpotekaModelViewSet, basename='offer')


urlpatterns = [
    path('', include(routers.urls))
]
