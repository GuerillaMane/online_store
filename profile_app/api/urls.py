from rest_framework import routers
from django.conf.urls import include
from django.urls import path

from . import views

router = routers.DefaultRouter()
router.register('user', views.UserViewSet)
router.register('profile', views.ProfileViewSet)


urlpatterns = [
    path('', include(router.urls))
]
