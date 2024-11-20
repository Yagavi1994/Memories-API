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
        followed_id = serializer.validated_data.get('followed')
        print(f"Follow request received for Profile ID: {followed_id}")
        
        # Verify if the profile exists
        try:
            followed_user = User.objects.get(pk=followed_id)
            print(f"Followed User Found: {followed_user}")
        except User.DoesNotExist:
            print(f"User with ID {followed_id} does not exist.")
            raise serializers.ValidationError({'followed': 'Invalid PK - User does not exist.'})
        
        serializer.save(owner=self.request.user)


class FollowerDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a follower or unfollow a user if the request user is the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer