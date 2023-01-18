from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import StationSerializer
from .models import Station
from common.decorators.admin_decorator import admin_required
from common.decorators.auth_decorator import auth_required


class StationViewSet(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin
):

    serializer_class = StationSerializer
    queryset = Station.objects.all()

    @auth_required
    @admin_required
    @action(detail=False, methods=["post"], name="Create Station")
    def create_station(self, request, format=None):
        try:
            station = self.serializer_class(data=request.data)
            station.is_valid(raise_exception=True)
            station.save()
            return Response(
                status=status.HTTP_201_CREATED,
                data={
                    "message": "Station Created Successfully",
                    "station": station.validated_data,
                },
            )
        except Exception as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": True, "message": f"Couldn't create station: {e}"},
            )
