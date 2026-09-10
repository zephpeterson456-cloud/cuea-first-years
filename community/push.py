import json

from django.conf import settings

from pywebpush import webpush, WebPushException

from .models import PushSubscription


def send_push_notification(user, title, body, url="/"):
    subscriptions = PushSubscription.objects.filter(user=user)

    for subscription in subscriptions:
        try:
            webpush(
                subscription_info={
                    "endpoint": subscription.endpoint,
                    "keys": {
                        "p256dh": subscription.p256dh,
                        "auth": subscription.auth,
                    },
                },
                data=json.dumps({
                    "title": title,
                    "body": body,
                    "url": url,
                }),
                vapid_private_key=settings.VAPID_PRIVATE_KEY,
                vapid_claims={
                    "sub": settings.VAPID_EMAIL,
                },
            )

        except WebPushException as error:
            print(
                f"Push notification failed for "
                f"{user.username}: {error}"
            )
