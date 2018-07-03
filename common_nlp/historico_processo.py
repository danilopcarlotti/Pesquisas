from parserTextoJuridico import parserTextoJuridico
import pandas as pd, json, arrow

class historico_processo(parserTextoJuridico):
	"""Classe para obtenção de histórico do processo"""
	def __init__(self):
		super().__init__()
		self.historico = None

	def atualiza_historico(self, andamentos):
		for tribunal, data_pub, texto in andamentos:
			classe = self.classifica_texto(texto)
			if classe == 'Certidão':
				self.historico['certidões'].append((data_pub,tribunal, texto))
			elif classe == 'Agravo' or classe == 'Mandado de Segurança' or classe == 'Embargos declaratórios' or classe == 'Recurso':
				self.historico['recursos'].append((data_pub, tribunal, texto))
			elif classe == 'Movimento processual':
				self.historico['movimentações processuais'].append((data_pub,tribunal, texto))
			elif classe == 'Sentença' or classe == 'Homologação de acordo':
				self.historico['sentença'].append((data_pub, tribunal, texto))
			else:
				self.historico['outras movimentações'].append((data_pub,tribunal, texto))
		self.tempo_duracao()

	def atualiza_historico_existente(self, novos_andamentos, historico_p = None):
		# Para o caso de armazenar o histórico e posteriormente atualizá-lo com novos andamentos
		if historico_p:
			self.load_historico(historico_p)
		self.atualiza_historico(novos_andamentos)

	def criar_historico(self, andamentos):
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