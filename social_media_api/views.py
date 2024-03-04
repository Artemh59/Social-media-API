from rest_framework import viewsets

from social_media_api.models import User, Profile, Post
from social_media_api.serializers import UserSerializer, ProfileSerializer, PostSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        queryset = Profile.objects.all()
        username = self.request.query_params.get("username")
        if username is not None:
            queryset = queryset.filter(user__username__icontains=username)
        return queryset


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
