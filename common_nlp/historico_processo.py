from parserTextoJuridico import parserTextoJuridico
import pandas as pd, json, arrow

class historico_processo(parserTextoJuridico):
	"""Classe para obtenção de histórico do processo"""
	def __init__(self):
		super().__init__()
		self.batch_publicacoes = 1000
		self.historico = None
		self.id_processo = None
		self.processos_analisados = []
		self.numero_processo = None

	def andamentos_id_regex(self, cursor, regex, upper_bound, lower_bound=0):
		for n in range(lower_bound, self.batch_publicacoes):
			publicacoes = self.download_publicacoes(cursor, n)
			for numero, texto in publicacoes:
				if numero not in self.processos_analisados and re.search(regex,texto):
					self.processos_analisados.append(numero)
		lista_numeros_procurar = '"'
		for p in self.processos_analisados:
			lista_numeros_procurar += p + '",'
		lista_numeros_procurar += '"'
		cursor.execute('SELECT id from diarios.numero_proc where numero in (%s);' % (lista_numeros_procurar))
		lista_ids = [i[0] for i in cursor.fetchall()]
		return lista_ids

	def atualiza_historico(self, andamentos):
		for tribunal, data_pub, texto, classe_publicacao in andamentos:
			if classe_publicacao == 'NULL' or classe_publicacao == '':
				classe = self.classifica_texto(texto)
			if classe == 'Certidão':
				self.historico['certidões'].append((data_pub,tribunal, texto))
			elif classe == 'Agravo' or classe == 'Mandado de Segurança' or classe == 'Embargos declaratórios' or classe == 'Recurso':
				self.historico['recursos'].append((data_pub, tribunal, texto))
			elif classe == 'Movimento processual':
				self.historico['movimentações processuais'].append((data_pub,tribunal, texto))
			elif classe == 'Sentença' or classe == 'Homologação de acordo':
				self.historico['sentença'].append((data_pub, tribunal, texto))
			elif classe == 'Liminar':
				self.historico['liminares'].append((data_pub, tribunal, texto))
			else:
				self.historico['outras movimentações'].append((data_pub,tribunal, texto))
		self.tempo_duracao()

	def atualiza_historico_existente(self, novos_andamentos, historico_p = None):
		# Para o caso de armazenar o histórico e posteriormente atualizá-lo com novos andamentos
		if historico_p:
			self.load_historico(historico_p)
		self.atualiza_historico(novos_andamentos)

	def criar_historico(self, andamentos):
		# FALTA

		# perícia
		# execução

		self.historico = {
			# tuples com (data,tribunal, texto)
			'audiencias' : [],
			# tuples com (data,tribunal, texto)
			'certidões' : [],
			# data única da última distribuição
			'distribuição' : None,
			# tuples com (data, tribunal, texto)
			'liminares' : [],
			# tuples com (data, tribunal, texto)
			'movimentações processuais' : [],
			# tuples com (data, tribunal, texto)
			'outras movimentações' : [],
			# tuples com (data, tribunal, texto)
			'recursos' : [],
			# tuple com (data, tribunal, texto)
			'sentença' : [],
			# dicionário com o tempo de duração do processo
			'tempo de duração' : {
				'Audiência a sentença' : None,
				'Citação a sentença' : None,
				'Distribuição a audiência' : None,
				'Distribuição a sentença' : None
			}
		}
		self.atualiza_historico(andamentos)

	def download_publicacoes(self, cursor, lower_bound):
		cursor.execute('SELECT numero, texto from diarios.publicacoes_diarias limit %s, %s' % (lower_bound, self.batch_publicacoes))
		dados = cursor.fetchall()
		return dados

	def historico_as_string(self):
		# para armazenar o histórico como um json
		return json.dumps(self.historico)

	def load_historico(self, historico):
		# para processar um histórico do processo
		self.historico = json.loads(historico)
	
	def tempo_duracao(self):
		# FALTA: 
		#  Saber como encontrar certidão ref a mandado de citação cumprido
		#  Saber como encontrar data de distribuição
		if not self.historico:
			return None
		data_distribuicao = None
		data_audiencia = None
		data_sentenca = None
		if self.historico['distribuição']:
			data_distribuicao = arrow.get(self.historico['distribuição'],'DD/MM/YYYY')
		if len(self.historico['audiencias']):
			data_audiencia = arrow.get(self.historico['audiencias'][-1][1],'DD/MM/YYYY')
		if len(self.historico['sentença']):
			data_sentenca = arrow.get(self.historico['sentença'][-1][1],'DD/MM/YYYY')
		if data_sentenca:
			if data_audiencia:
				self.historico['tempo de duração']['Audiência a sentença'] = (data_sentenca - data_audiencia).days
			if data_distribuicao:
				self.historico['tempo de duração']['Distribuição a sentença'] = (data_sentenca - data_distribuicao).days
		if data_distribuicao and data_audiencia:
			self.historico['tempo de duração']['Distribuição a audiência'] = (data_audiencia - data_distribuicao).days

def main():
	pass

if __name__ == '__main__':
	main()