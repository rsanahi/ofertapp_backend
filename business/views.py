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
    @author Anahi Ruiz (rs.anahi at gmail.com)
    @date 21-06-20
    @version 1.0.0

    """
    queryset = UserBusiness.objects.all().filter(soft_delete=False)
    serializer_class = BusinessSerializer
    filter_fields = ('nombre_local', 'fk_user', 'fk_user__username')
    permission_groups = {
        'list': ['Admin'],
        'create': ['_Public'],
        'actualizar': ['Business'],
        'detalle': ['Business'],
        'categoria': ['Business', 'Admin', 'User'],
        'actualizar_logo': ['Business']
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
            url_path='actualizar-logo', url_name='actualizar-logo')
    def actualizar_logo(self, request, *args, **kwargs):
        user = request.user
        instance = get_object_or_404(self.queryset, fk_user=user.pk)
        ruta_img = os.path.join(settings.MEDIA_ROOT, str(instance.logo))

        if os.path.exists(ruta_img) and str(instance.logo) != 'default/business.jpg':
            os.remove(ruta_img)
        
        serializer = BusinessImgSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail':serializer.data},
                status=status.HTTP_200_OK)

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
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=False,
        url_path='detalles', url_name='detalles')
    def detalle(self, request, *args, **kwargs):
        user = request.user
        instance = get_object_or_404(self.queryset, fk_user=user.pk)
        serializer = BusinessUpdateSerializer(instance)
        return Response(serializer.data)

    @action(methods=['get'], detail=False,
            url_path='categorias', url_name='categorias')
    def categoria(self, request, *args, **kwargs):
        categorias = BusinessCategories.objects.all()
        serializer = BusinessCategoriesSerializer(categorias,many=True)
        return Response({'categorias':serializer.data},
                status=status.HTTP_200_OK)

class OfertsViewset(viewsets.ModelViewSet):

    """
        Clase para administrar las ofertas
        @author Anahi Ruiz (rs.anahi at gmail.com)
        @date 25-08-20
        @version 1.0.0
    """

    queryset = Ofertas.objects.all().filter(soft_delete=False)
    serializer_class = OfertasSerializer
    filter_fields = ('titulo', 'fk_user__categoria', 'fk_user__username', 'deshabilitado')
    permission_groups = {
        'list': ['Business'],
        'create': ['Business'],
        'actualizar': ['Business'],
    }

    def create(self, request):
        user = request.user
        oferta = request.data.copy()
        try:
            oferta['fk_user'] = UserBusiness.objects.get(fk_user=user.pk).id
            oferta['img'] = oferta['logo']
        except Exception as e:
            print(e)
            raise exceptions.PermissionDenied('Este usuario no existe.')

        serializer = self.serializer_class(data=oferta)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)
