from rest_framework.routers import DefaultRouter

from .views import VisaTypeViewSet

router = DefaultRouter()
router.register("", VisaTypeViewSet, basename="visa-types")

urlpatterns = router.urls
