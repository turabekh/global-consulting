from rest_framework.routers import DefaultRouter

from .views import TourPackageViewSet

router = DefaultRouter()
router.register("", TourPackageViewSet, basename="tour-packages")

urlpatterns = router.urls
