from django.core.urlresolvers import reverse
from django.test import TestCase

from identity.models import TipoDocumento, Pais


# Create your tests here.
class UsuarioViewsTest(TestCase):
	def __before(self):
		pais = Pais()
		pais.nome = "Brasil"
		pais.sigla2 = "BR"
		pais.sigla3 = "BRL"
		tipo_documento = TipoDocumento()
		tipo_documento.pais_vigencia = pais
		tipo_documento.descricao = "Cadastro de Pessoa Física"
		tipo_documento.abreviacao = "CPF"
		Pais.save(pais)
		TipoDocumento.save(tipo_documento)

	def test_novo_usuarios(self):
		self.__before()
		response = self.client.get(reverse('identity:nova_pessoa'))
		self.assertTrue(response != None)
		self.assertEquals(response.status_code, 200)
		self.assertTrue(response.context != None)
		self.assertTrue(response.context['usuario'] != None)
