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
    If the target user's profile is private, a follow request is created instead of a direct follow.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    def perform_create(self, serializer):
        followed_user = serializer.validated_data['followed']

        # Check if the followed user's profile is private
        if followed_user.profile.is_private:
            # Check if a follow request already exists
            follow_request, created = FollowRequest.objects.get_or_create(
                requester=self.request.user,
                receiver=followed_user,
                defaults={'status': 'pending'}
            )

            if not created:
                raise serializers.ValidationError({"detail": "Follow request already exists."})
            
            return Response({"detail": "Follow request sent."}, status=status.HTTP_201_CREATED)

        # Directly follow the user if the profile is public
        serializer.save(owner=self.request.user)


class FollowerDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a follower or unfollow a user if the request user is the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Override destroy to provide a custom response for unfollowing.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Successfully unfollowed."}, status=status.HTTP_204_NO_CONTENT)
