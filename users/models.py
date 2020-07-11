from django.db import models
from django.contrib.auth.models import User
from utils.models import SoftDelete
from .constants import *

# Create your models here.

class UserClient(SoftDelete):
    """
    Clase para almacenar la data del usuario cliente

    @author Anahi Ruiz (rs.anahi at gmail.com)
    @date 21-06-20
    @version 1.0.0
    """

    fk_user = models.OneToOneField(User, on_delete=models.CASCADE)

    genero = models.PositiveIntegerField(choices=GENERO_CHOICES, default=4)

    telefono = models.CharField(max_length=20)

    class Meta:
        """!
        Clase de metadata
        """
        ordering = ('pk',)
        verbose_name = 'User Cliente'
        verbose_name_plural = 'Users Clientes'
        db_table = 'user_client'

    def __str__(self):
        """!
        Método de serialización
        """
        return self.fk_user.username