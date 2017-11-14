import sys, re
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjrs():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de São Paulo"""
	def __init__(self):
		self.link_inicial = 'http://www.tjrs.jus.br/busca/?tb=jurisnova&partialfields=tribunal%3ATribunal%2520de%2520Justi%25C3%25A7a%2520do%2520RS.(TipoDecisao%3Aac%25C3%25B3rd%25C3%25A3o|TipoDecisao%3Amonocr%25C3%25A1tica|TipoDecisao:null)&t=s&pesq=ementario.#main_res_juris'
		self.pesquisa_livre = '//*[@id="q"]'
		self.inteiro_teor = '//*[@id="cJuris"]'
		self.dia_julgamento_inicial = '//*[@id="dia1"]'
		self.dia_julgamento_final = '//*[@id="mes1"]'
		self.mes_julgamento_inicial = '//*[@id="ano1"]'
		self.mes_julgamento_final = '//*[@id="dia2"]'
		self.ano_julgamento_inicial = '//*[@id="mes2"]'
		self.ano_julgamento_final = '//*[@id="ano2"]'
		self.botao_pesquisar = '//*[@id="conteudo"]/form/div[1]/div/div/input'
		

		

