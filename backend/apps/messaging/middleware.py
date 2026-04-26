from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from channels.sessions import CookieMiddleware
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


@database_sync_to_async
def get_user(user_id: int):
    try:
        return User.objects.get(id=user_id, is_active=True)
    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        cookies = scope.get("cookies") or {}
        access_cookie_name = getattr(settings, "REST_AUTH", {}).get("JWT_AUTH_COOKIE", "gc-access")
        token = cookies.get(access_cookie_name)

        scope["user"] = AnonymousUser()
        if token:
            try:
                validated = AccessToken(token)
                user_id = validated.get("user_id")
                if user_id is not None:
                    scope["user"] = await get_user(user_id)
            except (InvalidToken, TokenError):
                pass

        return await super().__call__(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
    return CookieMiddleware(JWTAuthMiddleware(inner))
