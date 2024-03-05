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
        parts = self.request.path.split('/')
        post_id = parts[-2]
        return Post.objects.get(id=post_id)
