from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.permissions import IsUserProfile
from users.serializers import ForAuthUserSerializer, ForCreateUserSerializer


# Create your views here.


class UserListAPIView(generics.ListAPIView):
    serializer_class = ForAuthUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ForAuthUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = ForCreateUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(pk=user.id)


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ForCreateUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsUserProfile]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(pk=user.id)


class Logout(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
