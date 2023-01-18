from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from knox.models import AuthToken

from .models import User
from .serializers import UserSerializer, CreateUserSerializer, LoginSerializer
from common.utils.enums import USER_ROLES


class UserViewSets(
    viewsets.GenericViewSet,
):
    queryset = User.objects.none()
    serializer_class = UserSerializer

    @action(detail=False, methods=["post"], name="")
    def sign_up(self, request, format=None):
        try:
            request.data["role"] = USER_ROLES.CUSTOMER.value
            user = CreateUserSerializer(data=request.data)
            user.is_valid(raise_exception=True)
            created_user = user.save()
            token = AuthToken.objects.create(created_user)
            return Response(
                {"user": user.data, "token": token[1]},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": True, "message": f"Couldn't create account: {e}"},
            )

    @action(detail=False, methods=["post"], name="")
    def admin_sign_up(self, request, format=None):
        try:
            existing_admiin = User.objects.get(role=USER_ROLES.ADMIN.value)
            if existing_admiin:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"error": True, "message": f"Admin already exists"},
                )
            request.data["role"] = USER_ROLES.ADMIN.value
            user = CreateUserSerializer(data=request.data)
            user.is_valid(raise_exception=True)
            created_user = user.save()
            token = AuthToken.objects.create(created_user)
            return Response(
                {"user": user.data, "token": token[1]},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": True, "message": f"Couldn't create account: {e}"},
            )

    @action(detail=False, methods=["post"], name="")
    def sign_in(self, request, format=None):
        try:
            user = LoginSerializer(data=request.data)
            user.is_valid(raise_exception=True)
            existing_user = user.validated_data
            serialized_user = self.serializer_class(existing_user)

            return Response(
                {
                    "user": serialized_user.data,
                    "token": AuthToken.objects.create(existing_user)[1],
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": True, "message": f"Couldn't Sign In: {e}"},
            )
