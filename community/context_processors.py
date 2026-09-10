from .models import Notification


def notifications_count(request):
    if request.user.is_authenticated:
        return {
            "unread_notifications": Notification.objects.filter(
                recipient=request.user,
                is_read=False,
            ).count()
        }

    return {
        "unread_notifications": 0
    }

def push_notifications(request):
    from django.conf import settings
    return {
        "VAPID_PUBLIC_KEY": settings.VAPID_PUBLIC_KEY,
    }
