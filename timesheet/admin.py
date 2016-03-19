from django.contrib import admin
from .models import Pessoa, Documento, Usuario, Empresa, TipoDocumento, Pais

class UsuarioInline(admin.StackedInline):
	model = Usuario

class PessoaInline(admin.StackedInline):
	model = Pessoa

class PessoaAdmin(admin.ModelAdmin):
	inlines = [UsuarioInline]

class DocumentoAdmin(admin.ModelAdmin):
	inlines = [PessoaInline]

class UsuarioAdmin(admin.ModelAdmin):
	search_fields = ['login']
	list_filter = ['login', 'data_criacao']
	list_display = ['login', 'data_criacao']

class EmpresaAdmin(admin.ModelAdmin):
	pass

class TipoDocumentoAdmin(admin.ModelAdmin):
	pass

class PaisAdmin(admin.ModelAdmin):
	pass


admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(TipoDocumento, TipoDocumentoAdmin)
admin.site.register(Pais, PaisAdmin)
