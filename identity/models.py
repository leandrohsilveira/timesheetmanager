from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Pais(models.Model):
	nome = models.CharField(verbose_name="nome" ,max_length=200)
	sigla2 = models.CharField(verbose_name="sigla (2)", max_length=2)
	sigla3 = models.CharField(verbose_name="sigla (3)", max_length=3)

	def __str__(self):
		return "%s/%s" % (self.nome, self.sigla2)

	class Meta:
		verbose_name = "país"
		verbose_name_plural = "países"

class TipoDocumento(models.Model):
	descricao = models.CharField(verbose_name = "descrição", max_length = 200)
	abreviacao = models.CharField(verbose_name = "abreviação", max_length = 10)
	pais_vigencia = models.ForeignKey(Pais, verbose_name = "país de vigência")
	mascara = models.CharField(verbose_name = "máscara", max_length = 100)

	def __str__(self):
		return self.abreviacao

	class Meta:
		verbose_name = "tipo de documento"
		verbose_name_plural = "tipos de documentos"


class Documento(models.Model):
	tipo_documento = models.ForeignKey(TipoDocumento, verbose_name = "tipo do documento")
	codigo = models.CharField(verbose_name = "código", max_length = 50)
	def __str__(self):
		return "%s: %s" % (self.tipo_documento, self.codigo)

	class Meta:
		verbose_name = "documento"
		verbose_name_plural = "documentos"
		permissions = [
			("own_documento", "Pode gerenciar a própria entidade Documento")
		]

class Pessoa(models.Model):
	documento = models.OneToOneField(Documento, verbose_name = "documento")
	usuario = models.ForeignKey(User, verbose_name = "usuario")

	def __str__(self):
		return " %s" % (self.usuario.get_full_name())

	class Meta:
		verbose_name = "pessoa"
		verbose_name_plural = "pessoas"
		permissions = [
			("own_pessoa", "Pode gerenciar a própria entidade Pessoa"),
			("can_see_pessoas_list", "Pode visualizar todas as pessoas")
		]

class Empresa(models.Model):
	razao_social = models.CharField(verbose_name = "razão social", max_length = 200)
	nome_fantasia = models.CharField(verbose_name = "nome fantasia", max_length = 200)
	data_fundacao = models.DateTimeField(verbose_name = "data de fundação")
	inscricao_estadual = models.CharField(verbose_name = "inscrição estadual", max_length = 200)
	documento = models.OneToOneField(Documento, verbose_name = "documento")
	def __str__(self):
		return "%s (%s)" % (self.razao_social, self.nome_fantasia)

	class Meta:
		verbose_name = "empresa"
		verbose_name_plural = "empresas"
		permissions = [
			("own_empresas", "Pode gerenciar as próprias entidades Empresas")
		]
