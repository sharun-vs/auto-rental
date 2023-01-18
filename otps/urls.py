from rest_framework.routers import SimpleRouter

from .views import OtpViewSet

router = SimpleRouter()
router.register(r"", OtpViewSet, basename="otps")

urlpatterns = []
urlpatterns += router.urls
