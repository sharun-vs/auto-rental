from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
import pendulum

from .serializers import OtpSerializer
from .models import Otp
from common.utils.email_sender import EmailSender


class OtpViewSet(viewsets.GenericViewSet, EmailSender):
    serializer_class = None
    queryset = Otp.objects.none()

    @action(detail=False, methods=["post"], name="Send Otp")
    def send_otp(self, request, format=None):
        try:

            otp = OtpSerializer(data={"email": request.query_params["email"]})
            otp.is_valid(raise_exception=True)
            otp.save()
            self.send_otp(request.query_params["email"])
            return Response(
                status=status.HTTP_201_CREATED,
                data={"message": f"Otp send to your email successfully"},
            )
        except Exception as e:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={"error": True, "message": f"Couldn't send otp: {e}"},
            )

    @action(detail=False, methods=["post"], name="Verify Otp")
    def verify_otp(self, request, format=None):
        try:
            email, otp = request.data.values()
            existing_otp = Otp.objects.get(email=email, otp=otp)

            if existing_otp.expiry_at < pendulum.now():
                existing_otp.is_expired = True
                existing_otp.expiry_at = pendulum.now()
                existing_otp.save()
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"error": True, "message": f"Otp Expired"},
                )
            existing_otp.is_expired = True
            existing_otp.expiry_at = pendulum.now()
            existing_otp.save()
            return Response(
                status=status.HTTP_201_CREATED,
                data={"message": f"Otp verified."},
            )
        except Exception as e:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={"error": True, "message": f"Couldn't verify otp: {e}"},
            )
