import json, os, qrcode, sys
from django.conf import settings
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.serializers import UserSerializer, UserUpdateSerializer
from .models import *


class BusinessSerializer(serializers.ModelSerializer):
  """
  Clase para serializar la data de la empresa

  """

  fk_user = UserSerializer(many=False)

  class Meta:
    """!
    Clase de metadata
    """
    model = UserBusiness
    fields = ('pk', 'nombre_local', 'telefono', 'direccion', 'fk_user')

  def create(self, validated_data):
    """!

    """
    user_business = validated_data.pop("fk_user")
    with transaction.atomic():
      user = User.objects.create_user(**user_business)
      user.groups.add(2)
      business_info = UserBusiness.objects.create(**validated_data, fk_user=user)
    return business_info