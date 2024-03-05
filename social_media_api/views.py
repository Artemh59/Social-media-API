from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from social_media_api.models import Profile, Post
from social_media_api.serializers import (
    UserSerializer,
    ProfileSerializer,
    PostSerializer,
)


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ProfileListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Profile.objects.all()
        username = self.request.query_params.get("username")
        if username is not None:
            queryset = queryset.filter(user__username__icontains=username)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="username",
                description="Filter by profile username",
                required=False,
                type=str,
            ),
        ],
    )
    def list(self, request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)


class MyProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Post.objects.all()

        hashtag = self.request.query_params.get("hashtag")
        if hashtag:
            print(hashtag)
            return queryset.filter(hashtags__icontains=hashtag)

        users = self.request.user.profile
        serializer = ProfileSerializer(users)
        follows = serializer.data["follows"]
        return queryset.filter(profile__id__in=follows)

    def get_object(self):
        parts = self.request.path.split("/")
        post_id = parts[-2]
        return Post.objects.get(id=post_id)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="hashtag",
                description="Filter posts by hashtag",
                required=False,
                type=str,
            ),
        ],
    )
    def get(self, request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)


class MyPostsView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.profile.posts
