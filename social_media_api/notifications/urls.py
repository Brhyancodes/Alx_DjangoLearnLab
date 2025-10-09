from django.urls import path
from .views import NotificationListView, mark_notification_read, unread_notifications

urlpatterns = [
    path("", NotificationListView.as_view(), name="notifications-list"),
    path("<int:pk>/read/", mark_notification_read, name="mark-notification-read"),
    path("unread/", unread_notifications, name="unread-notifications"),
]
