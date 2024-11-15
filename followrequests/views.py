from rest_framework import generics, status
from rest_framework.response import Response
from .models import FollowRequest
from .serializers import FollowRequestSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class FollowRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = FollowRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FollowRequest.objects.filter(receiver=self.request.user, status='pending')

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)

class FollowRequestAcceptView(generics.UpdateAPIView):
    queryset = FollowRequest.objects.all()
    serializer_class = FollowRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        follow_request = self.get_object()
        follow_request.status = 'accepted'
        follow_request.save()
        return Response(status=status.HTTP_200_OK)

class FollowRequestDeclineView(generics.DestroyAPIView):
    queryset = FollowRequest.objects.all()
    permission_classes = [IsAuthenticated]

class FollowRequestCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Count the number of pending follow requests for the logged-in user
        count = FollowRequest.objects.filter(receiver=request.user, status='pending').count()
        return Response({"count": count})
