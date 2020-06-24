from django.db import models

class SoftDelete(models.Model):
    """
    Clase abstracta para mantener eliminado logico
    """
    soft_delete = models.BooleanField(default=False)

    class Meta:
        """
        Clase de metadata
        """
        abstract = True
