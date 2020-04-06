from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from .serializers import (
    UserSerializer,
    ProfileSerializer
)
from ..models import (
    Profile
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
