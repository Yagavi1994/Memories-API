from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import FollowRequest
from followers.models import Follower
from .serializers import FollowRequestSerializer

class FollowRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = FollowRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FollowRequest.objects.filter(receiver=self.request.user, status='pending')

    def perform_create(self, serializer):
        # Prevent duplicate follow requests
        if FollowRequest.objects.filter(
            requester=self.request.user,
            receiver=serializer.validated_data['receiver'],
            status='pending'
        ).exists():
            return Response(
                {"detail": "Follow request already sent."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(requester=self.request.user)

class FollowRequestAcceptView(generics.UpdateAPIView):
    queryset = FollowRequest.objects.all()
    serializer_class = FollowRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        follow_request = self.get_object()
        if follow_request.status != 'pending':
            return Response(
                {"detail": "Only pending requests can be accepted."},
                status=status.HTTP_400_BAD_REQUEST
            )
        follow_request.status = 'accepted'
        follow_request.save()
        
        # Create a Follower record
        Follower.objects.create(user=follow_request.requester, followed=follow_request.receiver)
        
        return Response(status=status.HTTP_200_OK)

class FollowRequestDeclineView(generics.DestroyAPIView):
    queryset = FollowRequest.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        follow_request = self.get_object()
        if follow_request.status != 'pending':
            return Response(
                {"detail": "Cannot decline a non-pending follow request."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

class FollowRequestCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Count the number of pending follow requests for the logged-in user
        count = FollowRequest.objects.filter(receiver=request.user, status='pending').count()
        return Response({"count": count})
