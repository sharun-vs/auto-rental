from rest_framework import serializers
from datetime import datetime, timedelta
from random import randint
import pendulum

from .models import Otp


class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ["email"]

    def create(self, validated_data):
        validated_data["expiry_at"] = pendulum.now().add(minutes=10)
        validated_data["otp"] = randint(100000, 999999)

        try:
            existing_otp = Otp.objects.get(email=validated_data["email"])
            if existing_otp.is_expired:
                return Otp.objects.create(**validated_data)
            return existing_otp
        except:
            return Otp.objects.create(**validated_data)
