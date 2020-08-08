from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *

from rest_framework import (
    viewsets, exceptions, status
)
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from utils.permissions import is_in_group

from .serializers import *

# Create your views here.
@permission_classes([IsAuthenticated])
def deleteSoft(object_instance):
    """
    Funcion para el borrado logico
    """
    object_instance.soft_delete = True
    object_instance.save()
    return object_instance

class BusinessViewset(viewsets.ModelViewSet):
    """
    Clase para gestionar la data de la empresa


    """
    queryset = UserBusiness.objects.all().filter(soft_delete=False)
    serializer_class = BusinessSerializer
    filter_fields = ('id_resto','nombre_local','fk_user')
    permission_groups = {
        'list': ['Admin'],
        'create': ['_Public'],
        'actualizar': ['Business'],
        'detalle': ['Business']
    }

    def get_serializer_class(self):
        if self.request.method in ['PUT']:
            return BusinessUpdateSerializer
        return self.serializer_class
    
    def create(self, request):
        business = request.data
        business['fk_user']['username'] = business['fk_user']['email']
        serializer = self.serializer_class(data=business)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)

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
        try:
            instance = UserBusiness.objects.get(fk_user=user.pk)
        except Exception as e:
            print(e)
            return Response(
                {'detail':'Este usuario no se encuentra registrado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer_class()
        serializer = serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print(e)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=False,
        url_path='detalles', url_name='detalles')
    def detalle(self, request, *args, **kwargs):
        user = request.user
        print(user)
        instance = get_object_or_404(self.queryset, fk_user=user.pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)