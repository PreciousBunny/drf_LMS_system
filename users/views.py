from rest_framework import generics
from users.models import User
from users.serializers import UserSerializer

# Create your views here.


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
