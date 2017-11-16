from crawlerJus import crawlerJus
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tj():
	"""Generic class with methods for crawler_jurisprudencia_tj's"""
	def __init__(self):
		crawlerJus.__init__(self)

	def download_jurisprudencia(self,driver,pesquisa_livre,data_julg_iniXP,data_julg_ini,data_julg_fimXP,data_julg_fim,botao_pesquisar,termo='acordam'):
		driver.find_element_by_xpath(pesquisa_livre).send_keys(termo)
		driver.find_element_by_xpath(data_julg_iniXP).send_keys(data_julg_ini)
		driver.find_element_by_xpath(data_julg_fimXP).send_keys(data_julg_fim)
		driver.find_element_by_xpath(botao_pesquisar).click()

	def extrai_texto_html(self,pagina):
		soup = BeautifulSoup(pagina,'lxml')
		for script in soup(["script", "style"]):
			script.extract()
		return soup.get_text()