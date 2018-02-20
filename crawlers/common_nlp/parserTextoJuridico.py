import re, sys

class parserTextoJuridico():
	"""Parser for analysing 'acórdãos'"""
	def __init__(self):
		pass

	def tipo_texto(self,texto):
		pass

	def divisao_acordao(self,texto):
		ementa = re.search(r'\nE\s*?M\s*?E\s*?N\s*?T\s*?A(.*?)\nA\s*?C\s*?.*?R\s*?D.*?O', texto, re.DOTALL)
		acordao = re.search(r'\nA\s*?C\s*?.*?R\s*?D\s*?.*?O(.*?)\nR\s*?E\s*?L\s*?A\s*?T\s*?.*?R\s*?I\s*?O', texto, re.DOTALL)
		relatorio = re.search(r'\nR\s*?E\s*?L\s*?A\s*?T\s*?.*?R\s*?I\s*?O(.*?)\nV\s*?O\s*?T\s*?O', texto, re.DOTALL)
		voto =re.search(r'\nV\s*?O\s*?T\s*?O(.*?)\nDesembargador', texto, re.DOTALL)
		partes_texto = [ementa,acordao,relatorio,voto]
		partes = []
		for p in partes_texto:
			if p:
				partes.append(p.group(1))
			else:
				partes.append('')
		return partes

	def valor_dano_moral(self,texto):
		search = re.search(r'danos? mora.{1,50}R\s*?\$?\s*?[\d\,\.]{0,30}|indeniza.{1,50}R\s*?\$?\s*?[\d\.\,]{1,30}|R\s*?\$\s*?[\d\.\,]{0,30}.{0,50}danos? mora', texto, re.DOTALL | re.IGNORECASE)
		if search:
			valor = re.search(r'R\$\s*?([\d\,\.]{1,30})',search.group(0), re.DOTALL | re.IGNORECASE)
			if valor:
				dano_moral = re.sub(r'\.(\d\d)$', r',$1', valor.group(1))
				if dano_moral[-1] == '.' or dano_moral[-1] == ',':
					return dano_moral[:-1]
				else:
					return dano_moral
		return False

if __name__ == '__main__':
	pass