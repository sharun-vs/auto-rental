from rest_framework import serializers

from .models import Vehicle
from stations.serializers import StationSerializer


class VehicleSerializer(serializers.ModelSerializer):
    station = StationSerializer(read_only=True)

    class Meta:
        model = Vehicle
        fields = "__all__"


class CreateVehicleSerializer(serializers.ModelSerializer):
    # name = serializers.CharField()
    # details = serializers.CharField()

    class Meta:
        model = Vehicle
        fields = "__all__"
