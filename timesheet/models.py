from django.db import models

# Create your models here.
class Pais(models.Model):
	nome = models.CharField(verbose_name="Nome" ,max_length=200)
	sigla2 = models.CharField(verbose_name="Sigla (2)", max_length=2)
	sigla3 = models.CharField(verbose_name="Sigla (3)", max_length=3)
	def __str__(self):
		return "%s/%s" % (self.nome, self.sigla2)

class TipoDocumento(models.Model):
	descricao = models.CharField(verbose_name="Descrição", max_length=200)
	abreviacao = models.CharField(verbose_name="Abreviação", max_length=10)
	pais_vigencia = models.ForeignKey(Pais, verbose_name="País de Vigência", blank=True, null=True)
	def __str__(self):
		return self.abreviacao

class Documento(models.Model):
	tipo_documento = models.ForeignKey(TipoDocumento, verbose_name="Tipo do documento")
	codigo = models.CharField(verbose_name="Código", max_length=50)
	def __str__(self):
		return "%d - %s: %s" % (self.id, self.tipo_documento, self.codigo)

class Pessoa(models.Model):
	nome = models.CharField(verbose_name="Nome", max_length=200)
	documento = models.OneToOneField(Documento, verbose_name="Documento")
	def __str__(self):
		return "%d - %s" % (self.id, self.nome)

class Empresa(models.Model):
	razao_social = models.CharField(verbose_name="Razão Social", max_length=200)
	nome_fantasia = models.CharField(verbose_name="Nome Fantasia", max_length=200)
	data_fundacao = models.DateTimeField(verbose_name="Data de Fundação")
	inscricao_estadual = models.CharField(verbose_name="Inscrição Estadual", max_length=200)
	documento = models.OneToOneField(Documento, verbose_name="Documento")
	def __str__(self):
		return "%d - %s (%s)" % (self.id, self.razao_social, self.nome_fantasia)

class Usuario(models.Model):
	login = models.CharField(verbose_name="Login", max_length=16)
	senha = models.CharField(verbose_name="Senha", max_length=200)
	data_criacao = models.DateTimeField(verbose_name="Data de Criação")
	pessoa = models.OneToOneField(Pessoa, verbose_name="Pessoa")
	def __str__(self):
		return "%d - %s -> Pessoa: %s" % (self.id, self.login, self.pessoa)
