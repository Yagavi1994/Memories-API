from django.urls import path
from milestones import views


urlpatterns = [
    path('milestones/', views.MilestoneList.as_view()),
    path('milestones/<int:pk>/', views.MilestoneDetail.as_view()),
    path('milestones/<int:id>/edit/', views.MilestoneUpdate.as_view(), name='milestone-update'),
]
