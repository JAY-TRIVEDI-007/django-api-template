from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.conf import settings as djoser_settings
from rest_framework.validators import UniqueValidator
from djoser import serializers as djoser_serializers

User = get_user_model()


class UserSerializer(djoser_serializers.UserSerializer):
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "is_staff", "is_superuser")
        ref_name = "UserProfile"


class UserCreateSerializer(djoser_serializers.UserCreateSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            djoser_settings.LOGIN_FIELD,
            djoser_settings.USER_ID_FIELD,
            "password",
            "username"
        )
