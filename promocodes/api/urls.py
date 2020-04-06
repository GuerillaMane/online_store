from rest_framework import routers
from django.conf.urls import include
from django.urls import path

from . import views

router = routers.DefaultRouter()
router.register('promocode', views.PromoCodeViewSet)


urlpatterns = [
    path('', include(router.urls))
]
