from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from .models import FollowRequest
from followers.models import Follower
from .serializers import FollowRequestSerializer


from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import FollowRequest
from .serializers import FollowRequestSerializer


class FollowRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = FollowRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only the follow requests for the logged-in user
        return FollowRequest.objects.filter(receiver=self.request.user, status="pending")

    def perform_create(self, serializer):
        receiver = serializer.validated_data['receiver']

        # Prevent sending a follow request to yourself
        if self.request.user == receiver:
            raise ValidationError("You cannot send a follow request to yourself.")

        # Check if a follow request already exists
        existing_request = FollowRequest.objects.filter(
            requester=self.request.user,
            receiver=receiver
        ).first()

        if existing_request:
            # Handle existing follow requests based on their status
            if existing_request.status == "accepted":
                raise ValidationError("You are already following this user.")
            elif existing_request.status == "pending":
                raise ValidationError("A follow request is already pending.")
            elif existing_request.status in ["declined", "unfollowed"]:
                # Update the declined or unfollowed request to pending
                existing_request.status = "pending"
                existing_request.save()
                return Response(
                    {"detail": "Follow request has been resent."},
                    status=status.HTTP_200_OK,
                )

        # If no existing request, create a new follow request
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
            owner=follow_request.requester,
            followed=follow_request.receiver
        )

        # Delete the follow request after accepting
        follow_request.delete()

        return Response({"detail": "Follow request accepted and removed."}, status=status.HTTP_200_OK)


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
