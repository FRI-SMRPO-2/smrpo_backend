from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


class TokenAuthenticationView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        try:
            token = Token.objects.get(key=result.data.get('token'))
            update_last_login(None, token.user)
        except Exception as exc:
            return None
        return result
