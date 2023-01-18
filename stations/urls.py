from rest_framework.routers import SimpleRouter

from .views import StationViewSet

router = SimpleRouter()
router.register(r"", StationViewSet, basename="stations")

urlpatterns = []
urlpatterns += router.urls
