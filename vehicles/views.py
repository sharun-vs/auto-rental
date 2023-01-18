from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import VehicleSerializer, CreateVehicleSerializer
from .models import Vehicle
from common.decorators.auth_decorator import auth_required
from common.utils.enums import USER_ROLES
from common.decorators.admin_decorator import admin_required


class VehicleViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    serializer_class = VehicleSerializer

    def get_queryset(self):
        if (
            isinstance(self.request.user, AnonymousUser)
            or self.request.user.role == USER_ROLES.CUSTOMER.value
        ):
            return Vehicle.objects.filter(is_occupied=False, is_available=True)
        return Vehicle.objects.all()

    @auth_required
    @admin_required
    @action(detail=False, methods=["post"], name="Create Vehicle")
    def create_vehicle(self, request, format=None):
        try:
            vehicle = CreateVehicleSerializer(data=request.data)
            vehicle.is_valid(raise_exception=True)
            vehicle.save()
            return Response(
                status=status.HTTP_201_CREATED,
                data={
                    "message": "Vehicle Created SuccessFully",
                    "vehicle": vehicle.validated_data,
                },
            )
        except Exception as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": True, "message": f"Couldn't create vehicle: {e}"},
            )

    @auth_required
    @admin_required
    @action(detail=False, methods=["patch", "put"], name="Assign Station")
    def assign_station(self, request, format=None):
        try:
            vehicle_id, station_id = request.query_params.values()
            if not vehicle_id or not station_id:
                return Response(
                    status=status.HTTP_404_NOT_FOUND,
                    data={
                        "error": True,
                        "message": "Please Provide A Valid vehicle Id And Station Id",
                    },
                )
            Vehicle.objects.filter(uid=vehicle_id).update(station=station_id)
            return Response(
                status=status.HTTP_200_OK, data={"message": "Station assigned"}
            )
        except Exception as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": True, "message": f"Couldn't assign station: {e}"},
            )

    @auth_required
    @action(detail=False, methods=["put", "patch"], name="Pick A Vehicle")
    def pick_vehicle(self, request, format=None):
        try:
            if request.user.is_active == False:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={
                        "error": True,
                        "message": f"No User Found Or User Is Not Active.",
                    },
                )
            if not request.query_params or not request.query_params["vehicle_id"]:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={
                        "error": True,
                        "message": f"Please provide valid vehicle id.",
                    },
                )

            selected_vehicle = Vehicle.objects.get(
                uid=request.query_params["vehicle_id"]
            )
            if selected_vehicle.is_available is False or selected_vehicle.is_occupied:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={
                        "error": True,
                        "message": f"Selected vehicle is not available or is already occupied.",
                    },
                )

            selected_vehicle.occupied_by = request.user
            selected_vehicle.is_occupied = True
            selected_vehicle.save()

            return Response(
                status=status.HTTP_201_CREATED,
                data={"message": "Picked Vehicle Successfully"},
            )

        except Exception as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": True, "message": f"Couldn't pick vehicle: {e}"},
            )

    @auth_required
    @action(detail=False, methods=["put", "patch"], name="Return vehicle")
    def return_vehicle(self, request, format=None):
        try:
            if not request.query_params or not request.query_params["vehicle_id"]:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={
                        "error": True,
                        "message": f"Please provide valid vehicle id.",
                    },
                )
            vehicle = Vehicle.objects.get(uid=request.query_params["vehicle_id"])
            print(vehicle.occupied_by, request.user.uid)
            if vehicle.occupied_by != request.user:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"error": True, "message": f"Unauthorized"},
                )
            vehicle.is_occupied = False
            vehicle.occupied_by = None
            vehicle.save()

            return Response(
                status=status.HTTP_201_CREATED,
                data={"message": "Vehicle Returned Successfully"},
            )

        except Exception as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": True, "message": f"Couldn't return vehicle: {e}"},
            )
