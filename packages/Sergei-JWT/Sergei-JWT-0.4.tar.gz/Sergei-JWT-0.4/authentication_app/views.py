from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from django.contrib.auth import get_user_model

from authentication_app.utils.response_handler import response_handler
from authentication_app.JWT.core import AuthHandler


auth = AuthHandler()


class Health(APIView):
    """
     View to return health status of authentication app
     No permissions or authentication required
     """
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        return response_handler(content={"service status": "OK"})


class Generate(APIView):
    """
    View to generate JWT TOKEN
    """

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        user = request.user
        token = auth.get_tokens(user)
        return response_handler(content={"JWT Token": token})


class Validate(APIView):
    """
    Validates token and returns data
    """
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        token = request.headers.get('Authorization').split(' ')[1]
        if auth.check_token(token):
            return response_handler(content={"Error": "Received blacklisted token"})
        _, payload = auth.decode_token(token)
        if _:
            return response_handler(content={"Error": "Invalid Token"})

        return response_handler(content={"pyload": payload})


class Refresh(APIView):
    """
    View to refresh access token,
    Refresh token required
    """
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        refresh_token = request.headers.get('Authorization').split(' ')[1]
        if auth.check_token(refresh_token):
            return response_handler(content={"Error": "Received blacklisted token"})

        error, tokens = auth.refresh_token(refresh_token)
        return response_handler(content={"tokens": tokens})


class Revoke(APIView):
    """
    View to revoke tokens
    Tokens will be added to blacklisting db (postqresql | Redis | Mongo)
    """
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        token = request.headers.get("Authorization").split(" ")[1]
        if auth.check_token(token):
            return response_handler(content={"Error": "Received blacklisted token"})
        error = auth.blacklist_token(token)
        if not error:
            return response_handler({"status": "Token Blacklisted"})
        else:
            return response_handler({"status": "Error occured"})


class Test(APIView):
    """
    Tests the whole token functionalities and returns status
    """
    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        dummy_user = get_user_model().objects.get(username="demo")
        tokens = auth.get_tokens(dummy_user)
        error, _ = auth.decode_token(tokens['access'])
        error, _ = auth.decode_token(tokens['refresh'])
        error = auth.blacklist_token(tokens['refresh'])
        error, _ = auth.refresh_token(tokens['refresh'])
        if error:
            return response_handler(content={"status": "Test Failed"})
        return response_handler(content={"status": "OK"})
