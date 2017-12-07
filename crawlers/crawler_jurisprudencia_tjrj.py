import sys, re, time
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_tjmt():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Tocantins"""
	def __init__(self):
		self.link_inicial = 'http://www4.tjrj.jus.br/ejuris/ConsultarJurisprudencia.aspx'
		self.pesquisa_livre = '//*[@id="ContentPlaceHolder1_txtTextoPesq"]'
		# direito
		self.botao_pesquisar = '//*[@id="ContentPlaceHolder1_btnPesquisar"]'

	def download_tj(self):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_bt_xpath(self.pesquisa_livre).send_keys('direito')
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		