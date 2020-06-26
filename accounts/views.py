from django.contrib.auth import get_user_model
from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from accounts.serializers import UserSerializer


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer
