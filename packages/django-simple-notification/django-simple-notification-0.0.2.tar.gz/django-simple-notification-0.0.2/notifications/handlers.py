from typing import Dict

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer

channel_layer = get_channel_layer()


def send_message(message, user, type: str):
    notification = Notification.objects.create(user=user, content=message, type=type)

    async_to_sync(channel_layer.group_send)(
        get_user_inbox_key(notification.user.id),
        {
            'type': 'notification',
            'notification_type': type,
            'data': dict(NotificationSerializer(notification).data)
        }
    )


def receive_handler(data: Dict):
    print(data)


def get_user_inbox_key(user_id):
    return f'inbox_{user_id}'


def post_like_notification(message, user):
    send_message(message, user, 'like_post')


def new_offer_notification(message, user):
    send_message(message, user, 'new_offer')
