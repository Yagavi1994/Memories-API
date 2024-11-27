from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from memories.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    """
    List posts or create a post if logged in.
    The perform_create method associates the post with the logged-in user.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__followed__owner__profile',  # Posts by followed users
        'likes__owner__profile',  # Posts liked by specific profiles
        'owner__profile',  # Posts by specific profile
    ]
    search_fields = [
        'owner__username',  # Search by username
        'title',  # Search by title
    ]
    ordering_fields = [
        'likes_count',  # Order by number of likes
        'comments_count',  # Order by number of comments
        'likes__created_at',  # Order by like creation time
    ]

    def perform_create(self, serializer):
        """
        Associate the post with the logged-in user when creating.
        """
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
