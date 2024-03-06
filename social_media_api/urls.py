from django.urls import path

from social_media_api.views import (
    UserRegisterView,
    ManageUserView,
    MyProfileView,
    ProfileListView,
    PostListView,
    MyPostsView,
)


urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="create"),
    path("me/", ManageUserView.as_view(), name="me"),
    path("profiles/", ProfileListView.as_view(), name="profiles"),
    path("my-profile/", MyProfileView.as_view(), name="my-profile"),
    path("posts/", PostListView.as_view(), name="posts"),
    path("my-posts/", MyPostsView.as_view(), name="my-posts"),
]

app_name = "social_media_api"
