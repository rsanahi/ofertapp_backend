from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView

from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_social_auth.serializers import UserSerializer


# Create your views here.

class BaseDetailView(generics.RetrieveAPIView):
    permission_classes = IsAuthenticated,
    serializer_class = UserSerializer
    model = get_user_model()

    def get_object(self, queryset=None):
        return self.request.user


class UserTokenDetailView(BaseDetailView):
    authentication_classes = (TokenAuthentication, )