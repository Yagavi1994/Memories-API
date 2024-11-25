from django.db.models import Count
from rest_framework.response import Response
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from memories.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from followers.models import Follower
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from memories.settings import (
    JWT_AUTH_COOKIE, JWT_AUTH_REFRESH_COOKIE, JWT_AUTH_SAMESITE,
    JWT_AUTH_SECURE,
)

class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by Django signals.
    """
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        milestones_count=Count('owner__milestone', distinct=True), 
        followers_count=Count('owner__followed', distinct=True),  
        following_count=Count('owner__following', distinct=True)    
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile',
    ]
    ordering_fields = [
        'posts_count',
        'milestones_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve or update a profile.
    Only the owner can update their profile.
    """
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        milestones_count=Count('owner__milestone', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    )
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self):
        profile = super().get_object()
        user = self.request.user

        # Default visibility flags to True, allowing access to posts and milestones
        profile.can_view_posts = True
        profile.can_view_milestones = True

        # If profile is private and the user is not authorized, restrict posts and milestones
        if profile.is_private and not (
            user.is_authenticated and (
                user == profile.owner or 
                Follower.objects.filter(owner=user, followed=profile.owner).exists()
            )
        ):
            profile.can_view_posts = False
            profile.can_view_milestones = False

        return profile

    def perform_destroy(self, instance):
        # Delete the user when the profile is deleted
        if instance.owner:
            instance.owner.delete()
            response = Response()
            response.set_cookie(
                key=JWT_AUTH_COOKIE,
                value='',
                httponly=True,
                expires='Thu, 01 Jan 1970 00:00:00 GMT',
                max_age=0,
                samesite=JWT_AUTH_SAMESITE,
                secure=JWT_AUTH_SECURE,
            )
            response.set_cookie(
                key=JWT_AUTH_REFRESH_COOKIE,
                value='',
                httponly=True,
                expires='Thu, 01 Jan 1970 00:00:00 GMT',
                max_age=0,
                samesite=JWT_AUTH_SAMESITE,
                secure=JWT_AUTH_SECURE,
            )
            return response