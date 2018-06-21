import sys
sys.path.append('/home/danilo/Documents/Pesquisas/common_nlp')
from dicionario_marcadores import dicionario_marcadores
import re, sys

class parserTextoJuridico():
	"""Parser for analysing 'acórdãos'"""
	def __init__(self):
		self.re_artigo = r'[\s\.]?art[igo\.]*?\s*?\d+'
		self.re_lei = r'[\s\.]lei.{,10}[\d/]{1,20}[\.]?[\d]{,10}'
		self.re_paragrafo = r'(§[\s\dº]+).{1,10}[artleicltp]?'
		self.re_inciso = r'(inciso\s*?)[A-Z]{,5}([,\.]?)'
		self.re_completo = r'art[\.\s].{,30}|lei[\sn\.\d/]{,30}|inciso.{,30}'
		self.nomes_leis_alternativos = ['Constituição','CLT','CF','CPP','CP','CC']
		self.marcadores = dicionario_marcadores

	def calcula_valor_decisao(self, texto, tipo_decisao):
		# treinado para ações trabalhistas do TRT02
		if tipo_decisao == 'acordo':
			textoValor = re.search(r'o valor.*?acordo.*?R\$\s*[\d\.,]{1,30}',texto)
		elif tipo_decisao == 'condenacao':
			textoValor = re.search(r'calculad.*? sobre.*?R\$\s*[\d.,]{1,30}.{1,30}condenação|calculad.*? sobre o valor.*?condenação.*?R\$\s*[\d\.,]{1,30}',texto)
		else:
			raise ValueError('Tipo de decisão não conhecido')
		if textoValor != None:
			valor = re.search(r'R\$\s*?[\d.,]{1,20}',textoValor.group(0))
			if valor != None:
				valor = valor.group(0).strip().replace('R','').replace('$','').replace('.','').replace(',','')
				try:
					valor = float(valor[:-2])
					return valor
				except:
					return False
		return False

	def classifica_texto(self, texto):
		# Treinado com um set de decisões trabalhistas
		acordo = re.search(r'homolog[oar\-se]\s*o\s*acordo',texto, re.IGNORECASE)
		if acordo != None:
			return 'Homologação de acordo'
		recurso = re.search(r'RECORRENTE',texto)
		if recurso != None:
			return 'Recurso'
		agravo = re.search(r'AGRAVANTE',texto)
		if agravo != None:
			return 'Agravo'
		ms = re.search(r'IMPETRANTE',texto)
		if ms != None:
			return 'Mandado de segurança'
		sentencaAnexa = re.search(r'SENTENÇA EM PDF',texto)
		if sentencaAnexa != None:
			return 'Sentença anexa'
		movimentoProcessual = re.search(r'Registre-se o movimento processual',texto,re.IGNORECASE)
		if movimentoProcessual != None:
			return 'Movimento processual'
		sentenca1 = re.search(r'TERMO DE AUDIÊNCIA',texto)
		embargos = re.search(r'embargos declaratórios',texto, re.IGNORECASE)
		embargos2 = re.search(r'embargos de declaração',texto, re.IGNORECASE)
		embargos3 = re.search(r'embargante',texto, re.IGNORECASE)
		if (embargos != None or embargos2 != None or embargos3 != None) and sentenca1 == None:
			return 'Embargos declaratórios'
		sentenca = re.search(r'\s*S\s*E\s*N\s*T\s*E\s*N\s*Ç\s*A\s*',texto)
		sentenca2 = re.search(r'Dispensado o relatório',texto)
		sentenca3 = re.search(r'FUNDAMENTAÇÃO',texto)
		sentenca4 = re.search(r'DISPOSITIVO',texto)
		if sentenca != None or sentenca1 != None or sentenca2 != None or (sentenca3 != None and sentenca4 != None):
			return 'Sentença'
		certidao = re.search(r'C\s*E\s*R\s*T\s*I\s*D\s*Ã\s*O',texto)
		if certidao != None:
			return 'Certidão'
		return 'NDA'

	def indicaResultado(self,texto, tipo):
		# Procedência ou não da ação
		# Treinado para ações trabalhistas do TRT02
		resultado = []
		if tipo == 'Sentença':
			# VETOR RESULTADO SENTENÇA POSSUI 4 POSIÇÕES (IMPROCEDENTE, PARCIALMENTE PROCEDENTE, PROCEDENTE, EXTINTO)
			resultado = [0,0,0,0]
			resultadoProcesso = re.search(r'julg.{1,30}IMPROCEDE',texto,re.IGNORECASE)
			resultadoProcessop = re.search(r'julg.*{1,30} PROCEDE',texto,re.IGNORECASE)
			resultadoProcessopp = re.search(r'julg.*{1,30}PARCIALMENTE\s*PROCEDENTE[S\s]?',texto,re.IGNORECASE)
			resultadoExtincao = re.search(r'julg.{1,30}extin[guirtoa]?',texto,re.IGNORECASE)
			if resultadoProcesso:
				resultado[0] = 1 
			if resultadoProcessop:
				resultado[2] = 1
			if resultadoProcessopp or (resultado[2] and resultado[0]):
				resultado[1] = 1
				resultado[0] = 0
				resultado[2] = 0
			if resultadoExtincao and resultado[0] == 0 and resultado[1] == 0 and resultado[2] == 0:
				resultado[3] = 1
		elif tipo == 'Recurso':
			# VETOR RESULTADO RECURSOS POSSUI 5 POSIÇÕES
			# (INTEMPESTIVO, NÃO CONHECIDO, CONHECIDO E PROVIDO, CONHECIDO E NEGADO, CONHECIDO PARCIALMENTE PROVIDO)
			resultado = [0,0,0,0,0]
			# Caso em que o resultado aparece no corpo do acórdão
			resultadoProcesso = re.findall(r'ACORDAM(.+)\.',texto, flags=re.IGNORECASE|re.DOTALL)
			if len(resultadoProcesso):
				for r in resultadoProcesso:
					if re.search(r'intempestivo',r, flags=re.IGNORECASE|re.DOTALL) != None:
						resultado[0] = 1
					else:
						if re.search(r'(NÃO CONHECER.{1,30}DO RECURSO)|(RECURSO NÃO CONHECIDO)|RECURSO DESPROVIDO',r, flags=re.IGNORECASE|re.DOTALL) != None:
							resultado[1] = 1
						elif re.search(r'CONHECER.{1,30}[D]?O[S]? RECURSO[S]?',r, flags=re.IGNORECASE|re.DOTALL) != None:
							if re.search(r'DAR PROVIMENTO|DOU PROVIMENTO', r, flags=re.IGNORECASE|re.DOTALL) != None:
								resultado[2] = 1
							elif re.search(r'NEGAR PROVIMENTO', r, flags=re.IGNORECASE|re.DOTALL) != None:
								resultado[3] = 1
						elif re.search(r'CONHECER.{1,30}E PROVER O[S]? RECURSO[S]?',r, flags=re.IGNORECASE|re.DOTALL) != None:
							resultado[2] = 1
						elif re.search(r'CONHECER.{1,30}E NEGAR[-LHES]? PROVIMENTO',r, flags=re.IGNORECASE|re.DOTALL) != None:
							resultado[3] = 1
						elif re.search(r'RECURSO PARCIALMENTE PROVIDO', r) != None:
							resultado[4] = 1
			# Caso em que o resultado aparece na ementa ou nada identificado no texto acima
			if resultado == [0,0,0,0,0]:
				if re.search(r'recurso.{1,30}intempestivo',texto, flags=re.IGNORECASE|re.DOTALL) != None:
					resultado[0] = 1
				else:
					if re.search(r'(NÃO CONHECER.{1,30}DO RECURSO)|(RECURSO NÃO CONHECIDO)|RECURSO DESPROVIDO|\.\s*?IMPROCEDÊNCIA\.',texto, flags=re.IGNORECASE|re.DOTALL) != None:
						resultado[1] = 1
					else:
						conhecer = re.search(r'CONHECER [D]?O[S]? RECURSO[S]?(.*?)\.',texto, flags=re.IGNORECASE|re.DOTALL)
						conhecer_1 = re.search(r'RECURSO CONHECIDO(.*?)\.',texto, flags=re.IGNORECASE|re.DOTALL)
						if conhecer and conhecer.group(1) != None:
							if re.search(r'(DAR PROVIMENTO)|( PROVIDO)|(DOU PROVIMENTO)', conhecer.group(1)) != None:
								resultado[2] = 1
							elif re.search(r'(NEGAR PROVIMENTO)|( DESPROVIDO)', conhecer.group(1)) != None:
								resultado[3] = 1
						elif conhecer_1 and conhecer_1.group(1) != None:
							if re.search(r'(DAR PROVIMENTO)|( PROVIDO)|(DOU PROVIMENTO)', conhecer_1.group(1)) != None:
								resultado[2] = 1
							elif re.search(r'(NEGAR PROVIMENTO)|( DESPROVIDO)', conhecer_1.group(1)) != None:
								resultado[3] = 1
						elif re.search(r'RECURSO PARCIALMENTE PROVIDO', texto) != None:
							resultado[4] = 1
		return resultado

	def parser_acordao(self,texto, tipo):
		# Método que pode ser aplicada a sentenças e recursos atualmente
		# Treinado genericamente para decisões trabalhistas do TRT02
		n_processo = re.search(r'\d{7}[-\.]\d{2}[-\.]\d{4}[-\.]\d[-\.]\d{2}[-\.]\d{4}',texto)
		if n_processo != None:
			n_processo = n_processo.group(0)
		else:
			n_processo = re.search(r'\d{20}',texto,re.IGNORECASE)
			if n_processo != None:
				n_processo = n_processo.group(0)
			else:
				n_processo = re.search(r'\d{8}-\d{4}',texto,re.IGNORECASE)
				if n_processo != None:
					n_processo = n_processo.group(0)
				else:
					n_processo = 'NULL'
		# Vara
		if tipo == 'Sentença':
			vara = re.search(r'.*?Vara(.+)',texto, re.IGNORECASE)
			if vara != None:
				vara =  vara.group(0)
			else:
				vara = 'NULL'
		elif tipo == 'Recurso':
			vara = re.search(r'\d+. TURMA',texto, re.IGNORECASE)
			if vara != None:
				vara =  vara.group(0)
			else:
				vara = 'NULL'
		# Parte autora
		if tipo == 'Sentença':
			parte_autora = re.search(r'RECLAMANTE[s]?\s*:\s*(.+)',texto,re.IGNORECASE)
			if parte_autora != None:
				parte_autora = re.sub(r'RECLAMAD[OAS\(\)]?.+','',parte_autora.group(1))
			else:
				parte_autora = re.search(r'REQUERENTE[s]?\s*:\s*(.+)',texto,re.IGNORECASE)
				if parte_autora != None:
					parte_autora = re.sub(r'REQUERID[OAS\(\)]?.+','',parte_autora.group(1))
				else:
					parte_autora = re.search(r'autor[aes\s\(\)]?\s*:\s*(.+)',texto,re.IGNORECASE)
					if parte_autora != None:
						parte_autora = re.sub(r'R[ée][us\(\)\s]?\s*:.+','',parte_autora.group(1),re.IGNORECASE)
					else:
						parte_autora = re.search(r'exequente.[s]?\s*:\s*(.+)',texto,re.IGNORECASE)
						if parte_autora != None:
							parte_autora = re.sub(r'EXECUTAD[oas\(\)]?.+','',parte_autora.group(1),re.IGNORECASE)
						else:
							parte_autora = re.search(r'Reclamant[es]?\s*:\s*(.+)',texto,re.IGNORECASE)
							if parte_autora != None:
								parte_autora = parte_autora.group(1)
							else:
								parte_autora = 'NULL'
		elif tipo == 'Recurso':
			parte_autora = re.search(r'RECORRENTE[S]?:(.+)',texto)
			if parte_autora != None:
				parte_autora = parte_autora.group(1)
			else:
				parte_autora = 'NULL'
		# Parte ré
		if tipo == 'Sentença':
			parte_re = re.search(r'RECLAMAD[OAS\(\)]?\s*:*\s*(.+)',texto,re.IGNORECASE)
			if parte_re != None:
				parte_re = parte_re.group(1)
			else:
				parte_re = re.search(r'REQUERID[OAS\(\)]\s*:*\s*(.+)',texto,re.IGNORECASE)
				if parte_re != None:
					parte_re = parte_re.group(1)
				else:
					parte_re = re.search(r'executad[oas\(\)]?\s*:\s*(.+)',texto,re.IGNORECASE)
					if parte_re != None:
						parte_re = parte_re.group(1)
					else:
						parte_re = re.search(r'R[ée](?!gião)(?!gional)[us]?\s*:*(.+)',texto,re.IGNORECASE)
						if parte_re != None:
							parte_re = parte_re.group(1)
						else:
							parte_re = re.search(r'Reclamad[oas\(\)]?\s*:\s*(.+)',texto,re.IGNORECASE)
							if parte_re != None:
								parte_re = parte_re.group(1)
							else:
								parte_re = 'NULL'
		elif tipo == 'Recurso':
			parte_re = re.search(r'RECORRIDO[S]?:(.+)',texto)
			if parte_re != None:
				parte_re = parte_re.group(1)
			else:
				parte_re = 'NULL'
		return (vara,parte_autora,parte_re,n_processo)

	def referencias_artigo(self,texto):
		res = re.search(self.re_artigo,texto,re.IGNORECASE)
		if res:
			res = re.search(r'\d+',res.group(0))
			if res:
				return res.group(0)
		return ''

	def referencias_completas(self,texto):
		# retorna todas as referências encontradas
		return re.findall(self.re_completo,texto,re.IGNORECASE)

	def referencias_inciso(self,texto):
		res = re.search(self.re_inciso,texto)
		if res:
			res = re.search(r'[A-Z]{1,5}',texto)
			if res:
				return res.group(0)
		return ''

	def referencias_lei(self,texto):
		res = re.search(self.re_lei,texto,re.IGNORECASE)
		if res:
			return res.group(0)
		else:
			for n in self.nomes_leis_alternativos:
				nome_lei = re.search(r''+n,texto)
				if nome_lei:
					return nome_lei.group(0)
		return ''

	def referencias_paragrafo(self,texto):
		res = re.search(self.re_paragrafo,texto,re.IGNORECASE)
		if res:
			res = re.search(r'\d+',res.group(0))
			if res:
				return res.group(0)
		return ''

	def referencias_texto(self,texto):
		resultado = []
		texto = texto.replace('\'',' ')
		texto = texto.replace('\"',' ')
		referencias = self.referencias_completas(texto)
		for r in referencias:
			dicionario = {'Lei' : '','Artigo' : '', 'Paragrafo' : '', 'Inciso' : ''}
			dicionario['Lei'] = self.referencias_lei(r)
			dicionario['Artigo'] = self.referencias_artigo(r)
			dicionario['Paragrafo'] = self.referencias_paragrafo(r)
			dicionario['Inciso'] = self.referencias_inciso(r)
			if dicionario['Lei'] != '' and dicionario not in resultado:
				resultado.append(dicionario)
		return resultado

	def separa_argumentos(self, texto):
		paragrafos = re.split(dicionario_marcadores['início de parágrafo'],texto)[1:]
		argumentos = []
		argumento_atual = []
		for p in paragrafos:
			if argumento_atual == []:
				argumento_atual.append(p)
			else:
				continuidade = False
				for exp in dicionario_marcadores['continuidade do argumento']:
					if not continuidade and re.search(exp, p, re.DOTALL):
						argumento_atual.append(p)
						continuidade = True
				if not continuidade:
					argumentos.append(argumento_atual)
					argumento_atual = [p]
		if argumento_atual != []:
			argumentos.append(argumento_atual)
		return argumentos

	def separa_texto_juridico(self,texto, separar_argumentos=False):
		partes_texto = {'relatorio':None,'fundamentação':None,'dispositivo':None}
		separacao_0 = re.split(self.marcadores['fundamentação_dispositivo'], texto)
		separacao_1 = re.split(self.marcadores['fundamentação'], texto)
		separacao_2 = re.split(self.marcadores['dispositivo'], texto)
		if len(separacao_0) == 3:
			partes_texto['relatorio'] = separacao_0[0]
			partes_texto['fundamentação'] = separacao_0[1]
			partes_texto['dispositivo'] = separacao_0[2]
		elif len(separacao_1) == 2:
			partes_texto['relatorio'] = separacao_1[0]
			fundamentos = separacao_1[1]
			separacao_2 = re.split(self.marcadores['dispositivo'], fundamentos)
			if len(separacao_2) == 2:
				partes_texto['fundamentação'] = separacao_2[0]
				partes_texto['dispositivo'] = separacao_2[1]
			else:
				partes_texto['fundamentação'] = fundamentos
		elif len(separacao_2) == 2:
				partes_texto['relatorio'] = separacao_2[0]
				partes_texto['dispositivo'] = ' '.join(separacao_2[1:])
		if separar_argumentos:
			for k,v in partes_texto.items():
				if v:
					partes_texto[k] = self.separa_argumentos(v)
		return partes_texto

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