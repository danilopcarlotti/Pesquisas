import sys, re, os
from common_nlp.parse_texto import busca
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class crawler_jurisprudencia_tjms():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Mato Grosso do Sul"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'https://www.tjms.jus.br/cjsg/resultadoCompleta.do'
		self.pesquisa_livre = '//*[@id="iddados.buscaInteiroTeor"]'
		self.data_julgamento_inicialXP = '//*[@id="iddados.dtJulgamentoInicio"]'
		self.data_julgamento_finalXP = '//*[@id="iddados.dtJulgamentoFim"]'
		self.botao_pesquisar = '//*[@id="pbSubmit"]'
		self.botao_proximo_ini = '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[5]'
		self.botao_proximo = '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[6]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_ms (ementas)'

	def parser_acordaos(self,texto,cursor):
		def parse(texto_decisao,cursor):
			numero = busca(r'\d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}', texto_decisao,ngroup=0)
			ementa = busca(r'\n\s*?E\s*?M\s*?E\s*?N\s*?T\s*?A\s*?\-(.+)', texto_decisao)
			classe_assunto = busca(r'Classe/Assunto\:\n\s*?(.+)', texto_decisao)
			classe = classe_assunto.split('/')[0]
			assunto = classe_assunto.split('/')[1]
			julgador = busca(r'\n\s*?Relator.*?\:\n\s*?(.+)', texto_decisao)
			orgao_julgador = busca(r'\n\s*?.rgão julgador\:\n\s*?\n\s*?(.+)', texto_decisao)
			origem = busca(r'\n\s*?Comarca\:\n\s*?\n\s*?(.+)',texto_decisao)
			data_disponibilizacao = busca(r'\n\s*?Data de publicação\:\n\s*?\n\s*?(\d{2}/\d{2}/\d{4})', texto_decisao)
			cursor.execute('INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, assunto, classe, data_decisao, orgao_julgador, julgador, texto_decisao, origem) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s");' % ('ms',numero, assunto, classe, data_disponibilizacao, orgao_julgador, julgador, ementa, origem))
		decisoes = re.split(r'\n\s*?\d\s*?\-\s*?\n',texto)
		for d in range(1,len(decisoes)):
			parse(decisoes[d],cursor)


# if __name__ == '__main__':
# 	c = crawler_jurisprudencia_tjms()
# 	print('comecei ',c.__class__.__name__)
# 	try:
# 		for l in range(len(c.lista_anos)):
# 			print(c.lista_anos[l],'\n')
# 			try:
# 				crawler_jurisprudencia_tj.download_tj_ESAJ_recaptcha(c,crawler_jurisprudencia_tj,'0101'+c.lista_anos[l],'3112'+c.lista_anos[l])
# 			except Exception as e:
# 				print(e)
# 	except Exception as e:
# 		print('finalizei o ano com erro ',e)

texto = '''
1 -


 
							
								
									



										0078840-02.2009.8.12.0001
									
 
										 

 										
										 


		E M E N T A - EMBARGOS DE DECLARAÇÃO - APELAÇÃO CÍVEL - AUSÊNCIA DE OMISSÃO, CONTRADIÇÃO OU OBSCURIDADE - REDISCUSSÃO - VIA ELEITA IMPRÓPRIA - LIMITES DO ART. 535 DO CÓDIGO DE PROCESSO CIVIL, MESMO PARA FINS DE PREQUESTIONAMENTO - EMBARGOS REJEITADOS. Os embargos de declaração destinam-se a suprir omissão, afastar obscuridade ou eliminar contradição. Portanto, ainda que tenham o propósito expresso de prequestionar dispositivos infraconstitucionais, sua viabilidade se submete à existência dos apontados vícios.   (TJMS. Embargos de Declaração n. 0078840-02.2009.8.12.0001,  Campo Grande,  1ª Câmara Cível, Relator (a):  Des. Joenildo de Sousa Chaves, j: 13/04/2011, p:  23/06/2016)
	


(1 ocorrência encontrada no inteiro teor do documento)





												Classe/Assunto:
											 Embargos de Declaração / Previdência privada											
										




										Relator(a):
									 Des. Joenildo de Sousa Chaves
									
								




										Comarca:
									 
									Campo Grande
								




										Órgão julgador:
									
									1ª Câmara Cível
								




										Data do julgamento:
									
									13/04/2011
								




										Data de publicação:
									
									23/06/2016
								




										Outros números:
									 
									78840022009812000150000
								




Ementa: E M E N T A - EMBARGOS DE DECLARAÇÃO - APELAÇÃO CÍVEL - AUSÊNCIA DE OMISSÃO, CONTRADIÇÃO OU OBSCURIDADE - REDISCUSSÃO - VIA ELEITA IMPRÓPRIA - LIMITES DO ART. 535 DO CÓDIGO DE PROCESSO CIVIL, MESMO PARA FINS DE PREQUESTIONAMENTO - EMBARGOS REJEITADOS. Os embargos de declaração destinam-se a suprir omissão, afastar obscuridade ou eliminar contradição. Portanto, ainda que tenham o propósito
											 	




Ementa: E M E N T A - EMBARGOS DE DECLARAÇÃO - APELAÇÃO CÍVEL - AUSÊNCIA DE OMISSÃO, CONTRADIÇÃO OU OBSCURIDADE - REDISCUSSÃO - VIA ELEITA IMPRÓPRIA - LIMITES DO ART. 535 DO CÓDIGO DE PROCESSO CIVIL, MESMO PARA FINS DE PREQUESTIONAMENTO - EMBARGOS REJEITADOS. Os embargos de declaração destinam-se a suprir omissão, afastar obscuridade ou eliminar contradição. Portanto, ainda que tenham o propósito expresso de prequestionar dispositivos infraconstitucionais, sua viabilidade se submete à existência dos apontados vícios. 
'''

c = crawler_jurisprudencia_tjms()
c.parser_acordaos(texto,1)