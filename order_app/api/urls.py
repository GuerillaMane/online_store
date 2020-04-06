from rest_framework import routers
from django.conf.urls import include
from django.urls import path

from . import views

router = routers.DefaultRouter()
router.register('order', views.OrderViewSet)
router.register('order_item', views.OrderItemViewSet)


urlpatterns = [
    path('', include(router.urls))
]
