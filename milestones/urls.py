from django.urls import path
from milestones import views


urlpatterns = [
    path('milestones/', views.MilestoneList.as_view()),
    path('milestones/<int:pk>/', views.MilestoneDetail.as_view()),
]