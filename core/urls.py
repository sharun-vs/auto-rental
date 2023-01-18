from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("vehicles/", include("vehicles.urls")),
    path("stations/", include("stations.urls")),
    path("otp/", include("otps.urls")),
]
