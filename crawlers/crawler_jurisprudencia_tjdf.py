from bs4 import BeautifulSoup
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from crawlerJus import crawlerJus
from common.conexao_local import cursorConexao
from selenium import webdriver
import sys, re, os, time, docx2txt

class crawler_jurisprudencia_tjdf(crawler_jurisprudencia_tj):
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Distrito Federal"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'https://pesquisajuris.tjdft.jus.br/IndexadorAcordaos-web/sistj?visaoId=tjdf.sistj.acordaoeletronico.buscaindexada.apresentacao.VisaoBuscaAcordao&nomeDaPagina=buscaLivre2&buscaPorQuery=1&baseSelecionada=BASE_ACORDAOS&ramoJuridico=&baseDados=[BASE_ACORDAOS,%%20TURMAS_RECURSAIS]&argumentoDePesquisa=a&filtroSegredoDeJustica=false&desembargador=&indexacao=&tipoDeNumero=NumAcordao&tipoDeRelator=TODOS&camposSelecionados=[ESPELHO]&numero=&tipoDeData=DataPublicacao&dataFim=&dataInicio=&ementa=&orgaoJulgador=&filtroAcordaosPublicos=false&legislacao=&numeroDaPaginaAtual=%s&quantidadeDeRegistros=20&totalHits=799443'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_df (ementas)'
		self.tabela_colunas_1_inst = 'justica_estadual.jurisprudencia_df_1_inst (sentencas)'
		
	def download_tj(self,ultima_pag):
		cursor = cursorConexao()
		for i in range(15000,ultima_pag):
			try:
				time.sleep(5)
				link = (self.link_inicial % str(i))
				driver = webdriver.Chrome(self.chromedriver)
				driver.get(link)
				lista_acordaos = driver.find_elements_by_id('id_link_abrir_dados_acordao')
				for i in range(len(lista_acordaos)):
					lista_acordaos_aux = driver.find_elements_by_id('id_link_abrir_dados_acordao')
					lista_acordaos_aux[i].click()
					divs_com_rotulo = driver.find_elements_by_class_name("conteudoComRotulo")
					links_inteiro_teor = divs_com_rotulo[-1].find_elements_by_tag_name('span')
					try:
						links_inteiro_teor[0].click()
					except:
						pass
					time.sleep(1)
					driver.find_element_by_id('id_comando_voltar_supra').click()
				driver.close()
			except Exception as e:
				print(e)

	def parser_acordaos(self, arquivo, cursor, pdf_class):
		text = docx2txt.process(arquivo)
		numero = busca(r'\n\s*?N.\s*?Processo\s*?\:(.*?)\n', texto)
		julgador = busca(r'\n\s*?Relator Des.\s*?\:(.*?)\n', texto)		
		data_decisao = busca(r'\n\s*?Brasília \(DF\)\, (.*?)\.', texto)
		orgao_julgador = busca(r'\n\s*?Órgãos\s*?\:(.*?)\n', texto)
		cursor.execute('INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, data_decisao, orgao_julgador, julgador, texto_decisao) values ("%s","%s","%s","%s","%s","%s");' % ('df',numero, data_decisao, orgao_julgador, julgador, texto))

def main():
	c = crawler_jurisprudencia_tjdf()

	cursor = cursorConexao()
	p = pdf_to_text()
	for arq in os.listdir(path+'/df_2_inst'):
		c.parser_acordaos(path+'/df_2_inst/'+arq, cursor, p)
	

	# print('comecei ',c.__class__.__name__)
	# try:
	# 	c.download_tj(40000) #número atualizado em jan 2018
	# except Exception as e:
	# 	print(e)

if __name__ == '__main__':
	main()