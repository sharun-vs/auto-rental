from rest_framework import serializers

from .models import Station


class StationSerializer(serializers.ModelSerializer):
    location = serializers.DictField(child=serializers.FloatField())

    class Meta:
        model = Station
        fields = "__all__"
