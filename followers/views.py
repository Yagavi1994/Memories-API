from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from memories.permissions import IsOwnerOrReadOnly
from .models import Follower
from .serializers import FollowerSerializer
from followrequests.models import FollowRequest

class FollowerList(generics.ListCreateAPIView):
    """
    List all followers or follow a user if logged in (for public profiles only).
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    def perform_create(self, serializer):
        followed_user = serializer.validated_data['followed']

        # Public profile logic only
        if followed_user.profile.is_private:
            raise serializers.ValidationError({"detail": "Cannot directly follow a private profile."})
        
        # Create a follower for public profiles
        serializer.save(owner=self.request.user)



class FollowerDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a follower or unfollow a user if the request user is the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer