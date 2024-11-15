from django.urls import path
from .views import FollowRequestListCreateView, FollowRequestAcceptView, FollowRequestDeclineView, FollowRequestCountView

urlpatterns = [
    path('follow-requests/', FollowRequestListCreateView.as_view(), name='follow-request-list-create'),
    path('follow-requests/<int:pk>/accept/', FollowRequestAcceptView.as_view(), name='follow-request-accept'),
    path('follow-requests/<int:pk>/decline/', FollowRequestDeclineView.as_view(), name='follow-request-decline'),
    path('follow-requests/count/', FollowRequestCountView.as_view(), name='follow-request-count'),
]
