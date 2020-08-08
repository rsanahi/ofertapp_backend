from django.db import models
from utils.models import SoftDelete
from django.contrib.auth.models import User

# Create your models here.
class UserBusiness(SoftDelete):
    """
    Clase para almacenar la data del usuario empresa

    @author Anahi Ruiz (rs.anahi at gmail.com)
    @date 21-06-20
    @version 1.0.0
    """
    fk_user = models.OneToOneField(User, on_delete=models.CASCADE)

    nombre_local = models.CharField(max_length=255, default="")

    direccion = models.CharField(max_length=500)

    telefono = models.CharField(max_length=20)

    class Meta:
        """!
        Clase de metadata
        """
        ordering = ('pk',)
        verbose_name = 'User Empresa'
        verbose_name_plural = 'Users Empresas'
        db_table = 'user_business'
        unique_together = (('nombre_local', 'fk_user'),)

    def __str__(self):
        """!
        Método de serialización
        """
        return self.fk_user.username
    
class Ofertas(SoftDelete):
    """
    Clase para almacenar las ofertas del usuario empresa

    @author Anahi Ruiz (rs.anahi at gmail.com)
    @date 21-06-20
    @version 1.0.0
    """
    fk_user = models.OneToOneField(UserBusiness, on_delete=models.CASCADE)

    titulo = models.CharField(max_length=255, default="", null=False)

    descripcion = models.TextField(max_length=255, default="")

    precio_neto = models.FloatField(null=False, default=0.00)

    porcentaje = models.IntegerField(null=False, default=0)