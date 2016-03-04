from django.db import models

# Create your models here.
class TipoDocumento(models.Model):
	descricao = models.CharField(max_length=200)
	abreviacao = models.CharField(max_length=10)
	def __str__(self):
		return self.abreviacao

class Documento(models.Model):
	tipo_documento = models.ForeignKey(TipoDocumento)
	codigo = models.CharField(max_length=50)
	def __str__(self):
		return "%d - %s: %s" % (self.id, self.tipo_documento, self.codigo)

class Pessoa(models.Model):
	nome = models.CharField(max_length=200)
	documento = models.ForeignKey(Documento)
	def __str__(self):
		return "%d - %s" % (self.id, self.nome)

class Empresa(models.Model):
	razao_social = models.CharField(max_length=200)
	nome_fantasia = models.CharField(max_length=200)
	data_fundacao = models.DateTimeField('data fundacao')
	inscricao_estadual = models.CharField(max_length=200)
	documento = models.ForeignKey(Documento)
	def __str__(self):
		return "%d - %s (%s)" % (self.id, self.razao_social, self.nome_fantasia)

class Usuario(models.Model):
	login = models.CharField(max_length=16)
	senha = models.CharField(max_length=200)
	data_criacao = models.DateTimeField('data criacao')
	pessoa = models.ForeignKey(Pessoa)
	def __str__(self):
		return "%d - %s -> Pessoa: %s" % (self.id, self.login, self.pessoa)
