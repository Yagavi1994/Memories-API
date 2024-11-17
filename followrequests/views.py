from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from .models import FollowRequest
from followers.models import Follower
from .serializers import FollowRequestSerializer


class FollowRequestListCreateView(generics.ListCreateAPIView):
    queryset = FollowRequest.objects.all()
    serializer_class = FollowRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Check if a follow request already exists between the requester and receiver
        existing_request = FollowRequest.objects.filter(
            requester=self.request.user,
            receiver=serializer.validated_data['receiver']
        ).first()

        if existing_request:
            # Handle existing follow requests based on their status
            if existing_request.status == "accepted":
                raise ValidationError("You are already following this user.")
            elif existing_request.status == "pending":
                raise ValidationError("A follow request is already pending.")
            else:
                # Update the existing request to pending
                existing_request.status = "pending"
                existing_request.save()
                return  # Skip creating a new request

        # Create a new follow request if none exists
        serializer.save(requester=self.request.user)


class FollowRequestAcceptView(generics.UpdateAPIView):
    queryset = FollowRequest.objects.all()
    serializer_class = FollowRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        follow_request = self.get_object()

        # Ensure only pending requests can be accepted
        if follow_request.status != "pending":
            raise ValidationError("Only pending requests can be accepted.")

        # Update the status to accepted
        follow_request.status = "accepted"
        follow_request.save()

        # Create a Follower entry upon acceptance
        Follower.objects.create(
            user=follow_request.requester,
            followed=follow_request.receiver
        )

        return Response({"detail": "Follow request accepted."}, status=status.HTTP_200_OK)


class FollowRequestDeclineView(generics.DestroyAPIView):
    queryset = FollowRequest.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        follow_request = self.get_object()

        # Ensure only pending requests can be declined
        if follow_request.status != "pending":
            raise ValidationError("Only pending requests can be declined.")

        # Delete the request
        follow_request.delete()

        return Response({"detail": "Follow request declined."}, status=status.HTTP_200_OK)


class FollowerDeleteView(generics.DestroyAPIView):
    queryset = Follower.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        follower_instance = self.get_object()

        # Update the FollowRequest status to "unfollowed" if it exists
        FollowRequest.objects.filter(
            requester=follower_instance.user,
            receiver=follower_instance.followed
        ).update(status="unfollowed")

        # Delete the follower relationship
        follower_instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowRequestCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Count the number of pending follow requests for the logged-in user
        count = FollowRequest.objects.filter(
            receiver=request.user,
            status='pending'
        ).count()
        return Response({"count": count})
