from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from memories.permissions import IsOwnerOrReadOnly
from .models import Follower
from .serializers import FollowerSerializer
from followrequests.models import FollowRequest

class FollowerList(generics.ListCreateAPIView):
    """
    List all followers or follow a user if logged in.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    def perform_create(self, serializer):
        followed_user = serializer.validated_data['followed']
        
        # Check if the followed user's profile is private
        if followed_user.profile.is_private:
            # Create a follow request instead of following directly
            FollowRequest.objects.get_or_create(
                requester=self.request.user, receiver=followed_user, status='pending'
            )
            return Response({"detail": "Follow request sent."}, status=status.HTTP_201_CREATED)
        else:
            # Directly follow the user if the profile is public
            serializer.save(owner=self.request.user)

class FollowerDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a follower or unfollow a user if the request user is the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
