import json, os, qrcode, sys
from django.conf import settings
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.serializers import UserSerializer, UserUpdateSerializer
from .models import *

class BusinessCategoriesSerializer(serializers.ModelSerializer):
	"""
		Clase para listar las categorias
	"""

	class Meta:
		"""
		"""
		model = BusinessCategories
		fields = '__all__'

class BusinessSerializer(serializers.ModelSerializer):
	"""
		Clase para serializar la data de la empresa
		@author Anahi Ruiz (rs.anahi at gmail.com)
		@date 25-08-20
		@version 1.0.0
	"""
	fk_user = UserSerializer(many=False)
	class Meta:
		"""!
		Clase de metadata
		"""
		model = UserBusiness
		fields = ('pk', 'nombre_local', 'telefono', 'fk_user')

	def create(self, validated_data):
		"""!

		"""
		user_business = validated_data.pop("fk_user")
		with transaction.atomic():
			user = User.objects.create_user(**user_business)
			user.groups.add(2)
			business_info = UserBusiness.objects.create(**validated_data, fk_user=user)
		return business_info


class BusinessUpdateSerializer(serializers.ModelSerializer):
	"""
		Clase para actualizar la data de la empresa
		@author Anahi Ruiz (rs.anahi at gmail.com)
		@date 25-08-20
		@version 1.0.0
	"""

	fk_user = UserUpdateSerializer(many=False)

	categoria = serializers.SlugRelatedField(
			slug_field='categoria',
			many=False,
			queryset=BusinessCategories.objects.all()
		)

	class Meta:
		"""
		"""
		model = UserBusiness
		exclude = ('created_at', 'updated_at')

	def update(self, instance, validated_data):
		"""!
		"""
		if validated_data.get("fk_user"):
			user_seri = validated_data.pop("fk_user")
		else:
			user_seri = {}
		instance.telefono = validated_data.get('telefono', instance.telefono)
		instance.nombre_local = validated_data.get('nombre_local', instance.nombre_local)
		instance.direccion = validated_data.get('direccion', instance.direccion)
		instance.categoria = validated_data.get('categoria', instance.categoria)
		instance.logo = validated_data.get('logo', instance.logo)

		email = user_seri.get('email') if user_seri.get('email', None) is not None else instance.fk_user.email        
		first_name = user_seri.get('first_name') if user_seri.get('first_name', None) is not None else instance.fk_user.first_name
		last_name = user_seri.get('last_name') if user_seri.get('last_name', None) is not None else instance.fk_user.last_name

		with transaction.atomic():
			user = instance.fk_user
			user.email = email
			user.first_name = first_name
			user.last_name = last_name
			user.save()
			instance.save()

		return instance

class BusinessImgSerializer(serializers.ModelSerializer):
	class Meta:
		"""
		Clase para serializar la data de las ofertas
		@author Anahi Ruiz (rs.anahi at gmail.com)
		@date 25-08-20
		@version 1.0.0
		"""
		model = UserBusiness
		fields = ('logo',)
  
	def update(self, instance, validated_data):
		"""!
	
		"""
		instance.logo = validated_data.get('logo', instance.logo)
		instance.save()
		return instance
    
class OfertasSerializer(serializers.ModelSerializer):
	class Meta:
		"""
		Clase para serializar la data de las ofertas
		@author Anahi Ruiz (rs.anahi at gmail.com)
		@date 25-08-20
		@version 1.0.0
		"""
		model = Ofertas
		exclude = ('created_at', 'updated_at')
	
	def update(self, instance, validated_data):
		"""
		Clase para actualizar una oferta

		@param self instancia de la clase
		@param instance objeto intanciado del modelo
		@param validated_data data validada
		@return la información instancia del objeto
		"""
		instance.titulo = validated_data.get('titulo', instance.titulo)
		instance.descripcion = validated_data.get('descripcion', instance.descripcion)
		instance.precio = validated_data.get('precio', instance.precio)
		instance.porcentaje = validated_data.get('porcentaje', instance.porcentaje)
		instance.cantidad = validated_data.get('cantidad', instance.cantidad)
		instance.moneda = validated_data.get('moneda', instance.moneda)
		instance.deshabilitado = validated_data.get('deshabilitado', instance.deshabilitado)

		instance.save()
		return instance