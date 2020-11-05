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
    filter_fields = ('titulo', 'fk_business__categoria', 'deshabilitado')
    search_fields = ('titulo', )
    ordering_fields = ('id', )

    permission_groups = {
        'list': ['Business'],
        'create': ['Business'],
        'update': ['Business'],
        'destroy': ['Business'],
    }

    def list(self, request):
        get_data = self.request.query_params
        queryset = super(OfertsViewset, self).filter_queryset(self.get_queryset())
        
        paginate = get_data.get('paginate', None)
        if paginate != '0' or paginate is None:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = {'count':queryset.count(), 'results':serializer.data}
        return Response(data)

    def create(self, request):
        user = request.user
        oferta = request.data.copy()
        try:
            oferta['fk_business'] = UserBusiness.objects.get(fk_user=user.pk).id

            logo = oferta.get('logo', None)
            if logo:
                oferta['img'] = oferta.get('logo', None)
        except Exception as e:
            print("error", e)
            raise exceptions.PermissionDenied('Este usuario no existe.')

        serializer = self.serializer_class(data=oferta)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)
    
    def update(self, request, pk=None, *args, **kwargs):
        user = request.user
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        if user.pk != instance.fk_business.fk_user.pk:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail':'Esta oferta no pertenece a este restaurate.'})
        else:
            try:
                data['fk_business'] = instance.fk_business.pk
                serializer = self.get_serializer(instance, data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data)
            except Exception as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail':'Error al actualizar la oferta'})
        
        return Response(status=status.HTTP_200_OK, data={'detail':'updated'})

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            instance = self.get_object()
            deleteSoft(instance)
            detail = {"detail": "Se eliminó con éxito el elemento: {0}".format(instance)}
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'detail':'Error al eliminar oferta.'})
        return Response(detail, status=status.HTTP_200_OK)