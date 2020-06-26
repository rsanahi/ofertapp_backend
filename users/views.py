from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import (
    viewsets, exceptions, status
)
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from utils.permissions import is_in_group

from .serializers import *
from .models import *

class UserViewset(viewsets.ModelViewSet):
    """
    Clase para gestionar la data del usuario
    
    @author Anahi Ruiz (rs.anahi at gmail.com)
    @date 24-06-20
    @version 1.0.0
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_fields = ('id', 'email', 'username')


class UserGroupSerializer(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserGroupSerializer

class UserClientViewset(viewsets.ModelViewSet):
    """
    Clase para gestionar la data del cliente

    @author Anahi Ruiz (rs.anahi at gmail.com)
    @date 24-06-20
    @version 1.0.0
    """
    queryset = UserClient.objects.all()
    serializer_class = UserClientSerializer
    filter_fields = ('id', 'genero', 'telefono')
    permission_groups = {
        'list': ['Admin'],
        'create': ['_Public'],
        'actualizar': ['User'],
        'detalle': ['User'],
    }

    @action(methods=['put'], detail=False,
            url_path='actualizar', url_name='actualizar')
    def actualizar(self, request, *args, **kwargs):
        """
        Funcion para actualizar datos del cliente

        @param request objeto de la peticion
        @return Response objeto del cliente actualizado
        """
        partial = kwargs.pop('partial', False)
        user = request.user

        self.serializer_class = UserClientUpdateSerializer
        print(user)
        try:
            instance = UserClient.objects.get(fk_user=user.pk)
        except Exception as e:
            print(e)
            return Response(
                {'detail':'Este usuario no se encuentra registrado'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(methods=['get'], detail=False,
            url_path='detalles', url_name='detalles')
    def detalle(self, request, *args, **kwargs):
        user = request.user
        instance = get_object_or_404(self.queryset, fk_user=user.pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)