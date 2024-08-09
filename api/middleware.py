from channels.middleware import BaseMiddleware
from django.conf import settings
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from jwt import decode as jwt_decode

User = get_user_model()


@database_sync_to_async
def get_user(validated_token):
    try:
        user = get_user_model().objects.get(id=validated_token["user_id"])
        return user
    except User.DoesNotExist:
        return AnonymousUser()


class WebSocketJWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            token_name, token_key = headers[b'authorization'].decode().split()
            if token_name == 'Bearer':
                decoded_data = jwt_decode(token_key, settings.SECRET_KEY, algorithms=[settings.SIMPLE_JWT['ALGORITHM']])
                scope["user"] = await get_user(validated_token=decoded_data)
        return await super().__call__(scope, receive, send)
