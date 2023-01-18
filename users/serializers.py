from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uid", "email", "is_staff", "is_active", "date_joined", "role"]


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return User.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        try:
            existing_user = User.objects.get(email=attrs["email"])
            is_passwords_match = check_password(
                attrs["password"], existing_user.password
            )
            if is_passwords_match:
                return existing_user
            raise serializers.ValidationError("Incorrect Credentials Passed.")
        except Exception as e:
            raise serializers.ValidationError(f"Couldn't Validate: {e}")
