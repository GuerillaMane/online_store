from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'id'
        )


class ProfileSerializer(serializers.ModelSerializer):
    user_obj = UserSerializer(
        source='user',
        read_only=True,
    )

    class Meta:
        model = Profile
        exclude = ('user',)
