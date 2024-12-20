from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from memories.permissions import IsOwnerOrReadOnly
from .models import Milestone
from .serializers import MilestoneSerializer


class MilestoneList(generics.ListCreateAPIView):
    """
    List milestones or create a milestone if logged in.
    The perform_create method associates the milestone with the logged-in user.
    """
    serializer_class = MilestoneSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Milestone.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'owner__profile',
    ]
    search_fields = [
        'owner__username',
        'title',
    ]
    ordering_fields = [
        'likes_count',
        'comments_count',
        'likes__created_at',
    ]

    def perform_create(self, serializer):
        """
        Save the milestone with the currently authenticated user as the owner.
        """
        serializer.save(owner=self.request.user)


class MilestoneDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a milestone and edit or delete it if you own it.
    """
    serializer_class = MilestoneSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Milestone.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
