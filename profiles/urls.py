from django.urls import path
from profiles import views

urlpatterns = [
    path('profiles/', views.ProfileList.as_view()),
    path('profiles/<int:pk>/', views.ProfileDetail.as_view()),
    path('profiles/<int:pk>/delete/', views.ProfileDeleteView.as_view(), name="profile-delete"),
    path("privacy-status/", views.PrivacyStatusView.as_view(), name="privacy-status"),
]