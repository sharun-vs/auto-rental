from rest_framework.routers import SimpleRouter

from .views import UserViewSets


router = SimpleRouter()
router.register(r"", UserViewSets, basename="users")

urlpatterns = []
urlpatterns += router.urls
