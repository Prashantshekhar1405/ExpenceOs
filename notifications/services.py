from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Notification

def create_notification(user, notification_type , title , message):
    notification = Notification.objects.create(
        user = user , 
        notification_type = notification_type , 
        title = title , 
        message = message
    )
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "send_notification",
            "notification" : {
                "id" : notification.id,
                "notification_type" : notification.notification_type,
                "title":notification.title,
                "message" : notification.message, 
                "is_read" : notification.is_read , 
                "created_at" : (notification.created_at.isoformat()),
            }
        }
    )
    return notification
