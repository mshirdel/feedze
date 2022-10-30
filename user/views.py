from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from user.models import User
from user.serializers import UserCreateSerializer, UserSerializer


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserCreateSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
