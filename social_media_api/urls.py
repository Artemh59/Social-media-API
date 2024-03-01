from rest_framework.routers import DefaultRouter

from social_media_api.views import (
    UserViewSet,
    ProfileViewSet,
)

router = DefaultRouter()
router.register("user", UserViewSet)
router.register("profile", ProfileViewSet)

urlpatterns = router.urls

app_name = "social_media_api"
