import functools
from rest_framework import status
from rest_framework.response import Response

from common.utils.enums import USER_ROLES


def admin_required(view_func):
    @functools.wraps(view_func)
    def wrapper(self, request=None, format=None):
        if request.user and request.user.role == USER_ROLES.ADMIN.value:
            return view_func(self, request)

        return Response(
            {"error": True, "message": "Unauthorized"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return wrapper
