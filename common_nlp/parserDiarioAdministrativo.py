import re



class parserDiarioAdministrativo():
	"""
	Classe com métodos auxiliares para parseamento de diários administrativos.
	Testes iniciais feitos com os diários de SP.
	"""
	def __init__(self):
		self.regex_ini_fim_publicacao = 
		r'\n\s*?Comunicados?\n\s*?Despacho|\n\s*?Extratos?.{1,50}Contratos?|\n\s*?Extratos?.{1,50}Termos?|\n\s*?Portaria|\n\s*?Resumos?.{1,50}Termos?|\n\s*?Resolução|\n\s*?AVISOS? DE LICITAÇÃO|\n\s*?Termos? de|\n\s*?.{1,30}HOMOLOGAÇÃO|\n\s*?JULGAMENTO|\n\s*?Ementa' #re.IGNORECASE
		self.regex_comunicado = [
			# Começo geral da descrição de itens comprados
			r'\n\s*?Processo.+',
			r'\n\s*?Objeto\:.*?\.\s*?\n', #re.DOTALL
			# Empresa responsável por comprar os itens abaixo
			r'\n\s*?Empresa\:.*?\.\s*?\n', #re.DOTALL
			# aqui começa a descrição dos itens comprados
			r'\n\s*?Item.*?\s*?\n',
			r'\n\s*?Quantidade[;\.]\s*?\n',
			r'\n\s*?Descrição\:.*?\.\s*?\n', #re.DOTALL
			r'\n\s*?Valor Unitário\:.*?\s*?\n',
			r'\n\s*?Valor Total\:.*?\s*?\n'
		],
		self.regex_extrato_contrato = [
			r'\n\s*?Termo de Contrato(.*?)Contratante(.*?)Contratad[oa](.*?)Objeto(.*?)Modalidade(.*?)Identificação Orçamentária(.*?)Fonte de Recursos(.*?)UGE(.*?)ND(.*?)Processo(.*?)Vigência(.*?)CNPJ(.*?)Número e data Parecer Jurídico(.*?)Valor(.*?)Data da assinatura(.*?)\n', #re.DOTALL
			r'\n\s*?Processo(.*?)Contrato(.*?)Resumo do Objeto(.*?)Data de Celebração do Termo de Contrato(.*?)Recurso Orçamentário(.*?)prazo de vigência(.*?)número e data do parecer jurídico e sigla(.*?)\.' #re.DOTALL
			r'\n\s*?Objeto\:(.*?)Mo-?da-?li-?da-?de(.*?)Va-?lor(.*?)Da-?ta de as-?si-?na-?tu-?ra do Con-?tra-?to\:(.*?)Fun-?cion-?nal Pro-?gra-?má-?ti-?ca\:(.*?)'
		],
