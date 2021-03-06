from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed 
from datetime import timedelta
from django.utils import timezone
from django.conf import settings


class ExpiringTokenAuthentication(TokenAuthentication):
    
    def expires_in(self, token):
        time_elapsed = timezone.now() - token.created
        left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time

    def is_token_expired(self, token):
        return self.expires_in(token) < timedelta(seconds = 0)

    def token_expire_handler(self, token):
        is_expired = self.is_token_expired(token)
        if is_expired:
            print("token expired")
        
        return is_expired

    def authenticate_credentials(self, key):
        message, token, user = None, None, None
        try:
            token = self.get_model().objects.select_related('user').get(key = key)
        except self.get_model().DoesNotExist:
            message = 'Invalid Token!'
        
        if not token.user.is_active:
            message = 'User is not active'

        is_expired = self.token_expire_handler(token)
        if is_expired:
            message = 'Token expired'
        
        return (token.user, token, message)