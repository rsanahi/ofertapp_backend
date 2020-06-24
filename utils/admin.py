from django.contrib import admin
from django.apps import apps

from .customMixin import ListAdminMixin

from .models import *


models = apps.get_models()
for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass

admin.site.site_header = 'Administración Ofertapp'

# Register your models here.
