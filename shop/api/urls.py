from rest_framework import routers
from django.conf.urls import include
from django.urls import path

from . import views

router = routers.DefaultRouter()
router.register('category', views.CategoryViewSet)
router.register('shop', views.ShopViewSet)
router.register('item', views.ItemViewSet)


urlpatterns = [
    path('', include(router.urls))
]
