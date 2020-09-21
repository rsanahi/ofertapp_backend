from django.db import models
from utils.models import SoftDelete
from django.contrib.auth.models import User
from django.utils import timezone

from .constants import *

# Create your models here.

class BusinessCategories(SoftDelete):
    """
    Clase para almacenar las categorias de empresas

    @author Anahi Ruiz (rs.anahi at gmail.com)
    @date 13-08-20
    @version 1.0.0
    """
    categoria = models.TextField(max_length=255, default="", null=False)
    
    descripcion = models.TextField(max_length=255, default="")

    class Meta:
        """!
        Clase de metadata
        """
        ordering = ('pk',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'business_categories'

    def __str__(self):
        """!
        Método de serialización
        """
        return self.categoria

class UserBusiness(SoftDelete):
    """
    Clase para almacenar la data del usuario empresa

    @author Anahi Ruiz (rs.anahi at gmail.com)
    @date 21-06-20
    @version 1.0.0
    """
    def get_upload_to(self, filename):
        return "business/%s/%s" % (self.fk_user.username, filename)

    fk_user = models.OneToOneField(User, on_delete=models.CASCADE)

    nombre_local = models.CharField(max_length=255, default="")

    logo = models.ImageField(upload_to=get_upload_to, null=True, blank=True, default='default/business.png')

    direccion = models.CharField(max_length=500)

    telefono = models.CharField(max_length=20)

    categoria = models.ForeignKey(BusinessCategories, on_delete=models.CASCADE, default=12)

    created_at = models.DateField(editable=False, default=timezone.now)

    updated_at = models.DateTimeField()

    class Meta:
        """!
        Clase de metadata
        """
        ordering = ('pk',)
        verbose_name = 'Business'
        verbose_name_plural = 'Users Business'
        db_table = 'user_business'
        unique_together = (('fk_user', 'nombre_local'),)

    def __str__(self):
        """!
        Método de serialización
        """
        return self.nombre_local
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(UserBusiness, self).save(*args, **kwargs)
    
class Ofertas(SoftDelete):
    """
    Clase para almacenar las ofertas del usuario empresa

    @author Anahi Ruiz (rs.anahi at gmail.com)
    @date 21-06-20
    @version 1.0.0
    """
    def get_upload_to(self, filename):
        return "oferts/%s/%s" % (self.fk_user.pk, filename)

    fk_user = models.ForeignKey(UserBusiness, on_delete=models.CASCADE,related_name="business_oferta")

    titulo = models.CharField(max_length=255, default="", null=False)

    descripcion = models.TextField(max_length=255, default="")

    precio = models.FloatField(null=False, default=0.00)

    porcentaje = models.IntegerField(null=False, default=0)
    
    cantidad = models.IntegerField(null=False, default=1)

    moneda = models.PositiveIntegerField(choices=MONEDA_CHOICES, default=4)

    img = models.ImageField(upload_to=get_upload_to, null=True, blank=True, default='default/oferta.png')

    deshabilitado = models.BooleanField(default=False)

    created_at = models.DateField(editable=False, default=timezone.now)

    updated_at = models.DateTimeField()

    class Meta:
        """!
        Clase de metadata
        """
        ordering = ('pk',)
        verbose_name = 'User Offer'
        verbose_name_plural = 'User Offers'
        db_table = 'business_offer'
        unique_together = (('fk_user', 'titulo'),)

    def __str__(self):
        """!
        Método de serialización
        """
        return self.titulo

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Ofertas, self).save(*args, **kwargs)