import jwt
from datetime import datetime
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from Sergei import settings
from authentication_app.utils.redis_helper import getTokenRedis, setTokenRedis

from authentication_app.models import BlacklistToken
from authentication_app.utils.userConfig import getPref

pref = getPref()


class AuthHandler():
    JWT_SECRET = settings.SERGEI['JWT']['SECRET']
    TTL = settings.SERGEI['JWT']['TTL']['access']
    REFRESH_TTL = settings.SERGEI['JWT']['TTL']['refresh']

    def encode_token(self, user, refresh_token=False):
        payload = {
            'exp': datetime.utcnow() + self.TTL,
            'iat': datetime.utcnow(),
            'grant_type': 'access',
            'id': user.id,
        }

        if refresh_token:
            payload['grant_type'] = 'refresh'
            payload['exp'] = datetime.utcnow() + self.REFRESH_TTL

        return jwt.encode(
            payload,
            self.JWT_SECRET,
            algorithm='HS256'
        )

    def decode_token(self, token: str):
        """
         Decodes and returns a token's payload, along with any error and the state
         state: Returns False if token is invalid or expired
         """
        error = None
        payload = None
        try:
            payload = jwt.decode(token, self.JWT_SECRET, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            error = jwt.ExpiredSignatureError
        except jwt.InvalidTokenError:
            error = jwt.InvalidTokenError
        return error, payload

    def get_tokens(self, user):
        """
         Returns a dict of tokens,
         user object must be valid, this function will not check whether the user object is valid or not.
            {
                access: "access-toke-here",
                refresh: "refresh-toke-here",
            }
         """
        tokens = {
            "access": self.encode_token(user),
            "refresh": self.encode_token(user, refresh_token=True)
        }
        return tokens

    def refresh_token(self, refresh_token: str):
        """
         Pass refresh tokens and get a new access token
         """
        error, payload = self.decode_token(refresh_token)
        if not error:
            user_id = payload['id']
            user = get_user_model().objects.get(id=user_id)
            token = self.get_tokens(user)
            return None, token
        elif error:
            pass
        return error, token

    def blacklist_token(self, token: str):

        error, payload = self.decode_token(token)
        if error:
            return error
        if pref['Blacklist_REQUIRED'] is True:
            try:
                user = get_user_model().objects.get(id=payload['id'])
                tokenObj = BlacklistToken(uuid=user, token=token)
                tokenObj.save()
            except Exception as error:
                return error
        if pref['USE_REDIS'] is True:
            setTokenRedis(token)

    def check_token(self, token: str):
        """
         Checks if a given token exists in the system and
         returns True if it is present else False
         """
        if pref['Blacklist_REQUIRED'] is False and pref['USE_REDIS'] is False:
            # No Blacklisting required return False
            return False

        if pref['Blacklist_REQUIRED'] is True:
            try:
                _ = BlacklistToken.objects.get(token=token)
                return True
            except ObjectDoesNotExist:
                return False

        elif pref['USE_REDIS'] is True:
            if getTokenRedis(token) is True:
                # Token in Redis
                return True
            else:
                return False
