from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "is_staff", "is_superuser")
        ref_name = "UserProfile"
