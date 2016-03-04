from django.contrib import admin
from .models import Pessoa, Documento, Usuario, Empresa, TipoDocumento, Pais

# Register your models here.
admin.site.register(Pessoa)
admin.site.register(Documento)
admin.site.register(Usuario)
admin.site.register(Empresa)
admin.site.register(TipoDocumento)
admin.site.register(Pais)
