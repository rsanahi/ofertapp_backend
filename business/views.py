from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *

from rest_framework import (
    viewsets, exceptions, status
)
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
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
    filter_fields = ('id_resto','nombre_local','fk_user','fk_user__username')
    permission_groups = {
        'list': ['Admin'],
        'create': ['_Public'],
    }