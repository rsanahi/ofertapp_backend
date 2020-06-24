import base64
import os
import shutil

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password, MinimumLengthValidator
from django.db import transaction

from rest_framework import serializers
from rest_framework.authtoken.models import Token


from djoser.serializers import SendEmailResetSerializer

from .models import *

class UserSerializer(serializers.ModelSerializer):
    """
    Clase para serializar la data del usuario

    @author Anahi Ruiz (rs.anahi at gmail.com)
    @date 24-06-20
    @version 1.0.0
    """
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        """!
        Clase de metadata
        """
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password']

    def validate(self, attrs):
        """!
        Clase para validar la data
        @param self instancia de la clase
        @param attrs atributos
        @return los atributos validados
        """
        user = User(**attrs)
        password = attrs.get('password')

        if User.objects.filter(email=attrs.get('email')):
            msg = "There is already a user with this email!"
            raise serializers.ValidationError({'email': msg})
        try:
            validate_password(password, user)
        except ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError({
                'password': serializer_error['non_field_errors']
            })
        return attrs

    def create(self, validated_data):
        """!
        Clase para crear el usuario
        @param self instancia de la clase
        @param validated_data data validada
        @return el usuario creado
        """
        try:
            user = User.objects.create_user(**validated_data)
        except IntegrityError:
            self.fail('cannot_create_user')
        return user

class UserGroupSerializer(serializers.ModelSerializer):
    """
    Clase para serializar el los grupos del usuario

    @author Anahi Ruiz (rs.anahi at gmail.com)
    @date 24-06-20
    @version 1.0.0
    """
    class Meta:
        """!
        Clase de metadata
        """
        model = User
        fields = ['username', 'groups']
        depth = 1

class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        """!
        Clase de metadata
        """
        model = User
        fields = ['email', 'username', 'first_name', 'last_name']
        read_only_fields = ('username',)

class UserClientSerializer(serializers.ModelSerializer):
    """
    Clase para serializar la data del usuario cliente

    @author Anahi Ruiz (rs.anahi at gmail.com)
    @date 24-06-20
    @version 1.0.0
    """
    fk_user = UserSerializer(many=False)

    class Meta:
        """!
        Clase de metadata
        """
        model = UserClient
        fields = ['telefono', 'genero', 'fk_user']


    def create(self, validated_data):
        """!
        Clase para crear el cliente

        @param self instancia de la clase
        @param validated_data data validada
        @return la información del cliente
        """
        user_seri = validated_data.pop("fk_user")
        with transaction.atomic():
            user = User.objects.create_user(**user_seri)
            user.groups.add(3)
            cliente = UserClient.objects.create(**validated_data, fk_user=user)
        return cliente


class UserClientUpdateSerializer(serializers.ModelSerializer):
    """
    Clase para serializar la data del usuario cliente

    @author Anahi Ruiz (rs.anahi at gmail.com)
    @date 24-06-20
    @version 1.0.0
    """
    fk_user = UserUpdateSerializer(many=False, required=False)

    class Meta:
        """!
        Clase de metadata
        """
        model = UserClient
        fields = ['telefono', 'genero', 'fk_user']


    def update(self, instance, validated_data):
        """!
        
        """
        if validated_data.get("fk_user"):
            user_seri = validated_data.pop("fk_user")
        else:
            user_seri = {}
        instance.telefono = validated_data.get('telefono', instance.telefono)
        email = user_seri.get('email') if user_seri.get('email', None) is not None else instance.fk_user.email        
        first_name = user_seri.get('first_name') if user_seri.get('first_name', None) is not None else instance.fk_user.first_name
        last_name = user_seri.get('last_name') if user_seri.get('last_name', None) is not None else instance.fk_user.last_name

        with transaction.atomic():
            user = instance.fk_user
            user.email=email
            user.first_name=first_name
            user.last_name=last_name
            user.save()
            instance.save()

        return instance

