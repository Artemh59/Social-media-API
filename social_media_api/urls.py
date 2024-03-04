from rest_framework.routers import DefaultRouter

from social_media_api.views import (
    UserViewSet,
    ProfileViewSet,
    PostViewSet,
)

router = DefaultRouter()
router.register("user", UserViewSet)
router.register("profile", ProfileViewSet, basename="profile")
router.register("posts", PostViewSet, basename="post")

urlpatterns = router.urls

app_name = "social_media_api"
