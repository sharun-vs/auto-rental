from rest_framework.routers import SimpleRouter

from .views import VehicleViewSet

router = SimpleRouter()
router.register(r"", VehicleViewSet, basename="vehicles")

urlpatterns = []
urlpatterns += router.urls
