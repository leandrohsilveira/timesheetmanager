from django.contrib import admin
from .models import Pessoa, Documento, Empresa, TipoDocumento, Pais

class PessoaAdmin(admin.ModelAdmin):
	pass

class DocumentoAdmin(admin.ModelAdmin):
	pass

class EmpresaAdmin(admin.ModelAdmin):
	pass

class TipoDocumentoAdmin(admin.ModelAdmin):
	pass

class PaisAdmin(admin.ModelAdmin):
	pass


admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(TipoDocumento, TipoDocumentoAdmin)
admin.site.register(Pais, PaisAdmin)
