import jwt
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from chat.models import ChatRoom, Message

User = get_user_model()


@database_sync_to_async
def get_user_from_jwt(token):
    try:
        # Decode the JWT token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.SIMPLE_JWT['ALGORITHM']])
        user_id = payload.get('user_id')

        if user_id:
            return User.objects.get(id=user_id)
    except (ExpiredSignatureError, InvalidTokenError):
        return None


# Define async functions for database operations
@database_sync_to_async
def get_or_create_user(user_id):
    return User.objects.get_or_create(id=user_id)


@database_sync_to_async
def get_or_create_chat_room(user):
    return ChatRoom.objects.get_or_create(user=user)


@database_sync_to_async
def get_messages(room):
    messages = Message.objects.filter(room=room).values('id', 'message', 'author', 'created_at')
    # Convert datetime objects to ISO format strings
    messages_list = []
    for message in messages:
        message_dict = dict(message)
        message_dict['created_at'] = message_dict['created_at'].isoformat()  # Convert datetime to ISO format string
        messages_list.append(message_dict)
    return messages_list


@database_sync_to_async
def message_create(room, author, message):
    Message.objects.create(room=room, author=author, message=message)
