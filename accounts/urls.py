from django.contrib import admin
from django.urls import path, include
from .views import CreateUserView

urlpatterns = [
    path('', include('rest_auth.urls')),
    path('sign-up/', CreateUserView.as_view(), name='register')
]
