import functools
from rest_framework import status
from rest_framework.response import Response


def auth_required(view_func):
    @functools.wraps(view_func)
    def wrapper(self, request=None, format=None):
        if self.request.method == "GET":
            if "Authorization" in self.request.headers:
                return view_func(self)
            raise Exception("Unauthorized")

        if "Authorization" in request.headers:
            return view_func(self, request, format=None)

        return Response(
            {"error": True, "message": "Unauthorized"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return wrapper
