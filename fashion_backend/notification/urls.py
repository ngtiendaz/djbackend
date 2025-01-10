from django.urls import path
from . import views



urlpatterns = [
    path('update/', views.UpdateNotification.as_view(), name="update-notification"),
    path('count/', views.GetNotificationCount.as_view(), name="count-notification"),
    path('me/', views.NotificationListView.as_view(), name="me-notification"),
]