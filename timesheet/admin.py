from django.contrib import admin
from .models import Pessoa, Documento, Usuario, Empresa, TipoDocumento

# Register your models here.
admin.site.register(Pessoa)
admin.site.register(Documento)
admin.site.register(Usuario)
admin.site.register(Empresa)
admin.site.register(TipoDocumento)
