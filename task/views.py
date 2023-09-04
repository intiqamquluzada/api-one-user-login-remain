import jwt
from django.utils import timezone
from django.contrib.auth import logout
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .serializers import LoginSerializer, RegisterSerializer
from task.models import MyUser as User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django.contrib.auth.models import AnonymousUser


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        user = User.objects.get(email=email)

        # if user.active_session:
        #     return Response({"error": "Hesabda adam var."}, status=400)

        token = RefreshToken.for_user(user)

        user.active_session = str(token.access_token)
        if not user.last_login_time or user.last_login_time < timezone.now():
            user.last_login_time = jwt.decode(token, None, ["HS256"])["exp"]
        user.save()

        data = {
            **serializer.data,
            "refresh": str(token),
            "access": str(token.access_token)
        }
        return Response(data, status=201)


class Logout(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
        user = request.user
        

        if user.is_authenticated:
            user.last_login_time = timezone.now()
            user.save()
        return Response(status=status.HTTP_200_OK)

class RemoveLog(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):

        return Response({"msg": "sdfsfsdf"}, status=status.HTTP_200_OK)


