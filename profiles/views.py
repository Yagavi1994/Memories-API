from django.db.models import Count
from rest_framework.response import Response
from rest_framework import generics, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from memories.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer
from followers.models import Follower
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from memories.settings import (
    JWT_AUTH_COOKIE, JWT_AUTH_REFRESH_COOKIE, JWT_AUTH_SAMESITE,
    JWT_AUTH_SECURE,
)


class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    Profile creation is handled by Django signals,
    so no create view is provided.
    """
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        milestones_count=Count('owner__milestone', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = [
        'owner__following__followed__profile',  # Profiles followed by the user
        'owner__followed__owner__profile',  # Profiles following the user
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
    Retrieve, update, or delete a profile.
    Only the owner can update or delete their profile.
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
        """
        Override to set visibility flags for posts
        and milestones based on privacy settings.
        """
        profile = super().get_object()
        user = self.request.user

        # Default visibility flags to True
        profile.can_view_posts = True
        profile.can_view_milestones = True

        # Restrict visibility if the profile is private,
        # And the user is not authorized
        if profile.is_private and not (
            user.is_authenticated and (
                user == profile.owner or
                Follower.objects.filter(owner=user, followed=profile.owner).exists()  # noqa
            )
        ):
            profile.can_view_posts = False
            profile.can_view_milestones = False

        return profile

    def destroy(self, request, *args, **kwargs):
        """
        Override to clear authentication cookies upon profile deletion.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        response = Response(status=status.HTTP_204_NO_CONTENT)
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

    def perform_destroy(self, instance):
        """
        Delete the associated user when the profile is deleted.
        """
        if instance.owner:
            instance.owner.delete()
