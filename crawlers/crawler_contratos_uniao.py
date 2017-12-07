import sys, re, threading, time
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao

c = crawlerJus()
cursor = conexao()

j = 352500
while j < 458000:
	print('comecei '+str(j))
	erros = 0
	pag = BeautifulSoup(c.baixa_pag('http://compras.dados.gov.br/licitacoes/v1/licitacoes.html?offset='+str(j)),'lxml')
	for l in pag.find_all('a', href=True):
		if re.search(r'/licitacoes/id/licitacao/\d+$',l['href']):
			i = l['href']
			licitacoes = []
			itens_licitacao = []
			contratos_licitacao = []
			aditivos = []
			# LICITAÇÕES DADOS
			pag = BeautifulSoup(c.baixa_pag('http://compras.dados.gov.br/' + i),'lxml')
			dados_licitacao = pag.find_all('p',attrs={'class':'inner'})[:-3]
			for d in range(len(dados_licitacao)):
				dados_licitacao[d] = dados_licitacao[d].get_text().replace('\'','').replace('\"','')
			licitacoes.append(dados_licitacao)
			# ITENS
			itens_link = []
			c.encontrar_links_html('http://compras.dados.gov.br/' + i, itens_link, r'/licitacoes/id/licitacao/\d+/itens')
			for it in itens_link:
				itens_l = []
				c.encontrar_links_html('http://compras.dados.gov.br/' + it, itens_l, r'/licitacoes/doc/licitacao/\d+/itens/\d+')
				for il in itens_l:
					#ITENS - DADOS
					pag_item = BeautifulSoup(c.baixa_pag('http://compras.dados.gov.br/' + il),'lxml')
					p_dados_itens = pag_item.find_all('p',attrs={'class':'inner'})
					for n in range(len(p_dados_itens)):
						p_dados_itens[n] = p_dados_itens[n].get_text().replace('\'','').replace('\"','')
					itens_licitacao.append(p_dados_itens)
			# CONTRATOS
			contratos_link = []
			c.encontrar_links_html('http://compras.dados.gov.br/' + i , contratos_link, r'/contratos/v1/contratos\?uasg_contrato=.+')
			for ccl in contratos_link:
				contratos_l = []
				c.encontrar_links_html('http://compras.dados.gov.br/' + ccl, contratos_l, r'/contratos/id/contrato/\d+$') 
				for cl in contratos_l:
					# CONTRATOS DADOS
					pag_contrato = BeautifulSoup(c.baixa_pag('http://compras.dados.gov.br/' + cl),'lxml')
					p_dados_contratos = pag_contrato.find_all('p',attrs={'class':'inner'}) # [:-3]
					for item in range(len(p_dados_contratos)):
						p_dados_contratos[item] = p_dados_contratos[item].get_text().replace('\'','').replace('\"','')
					contratos_licitacao.append(p_dados_contratos[:-3])
					# #  ADITIVOS
					pag_aditivos = []
					c.encontrar_links_html('http://compras.dados.gov.br/' + cl, pag_aditivos, r'/contratos/id/contrato/\d+/aditivos$')
					for p in pag_aditivos:
						links_aditivos  = []
						c.encontrar_links_html('http://compras.dados.gov.br/' + p, links_aditivos, r'/contratos/id/contrato/\d+/aditivos/\d+')
						# ADITIVOS DADOS
						for la in links_aditivos:
							pag_aditivo = BeautifulSoup(c.baixa_pag('http://compras.dados.gov.br/' + la),'lxml')
							dados_aditivos = pag_aditivo.find_all('p',attrs={'class':'inner'})
							for item in range(len(dados_aditivos)):
								dados_aditivos[item] = dados_aditivos[item].get_text().replace('\'','').replace('\"','')
							aditivos.append(dados_aditivos)
			for item in licitacoes:
				try:
					cursor.execute('INSERT INTO contratos_governo_federal.licitacoes (uasg, modalidade, numero_aviso, numero_identificador, situacao, tipo_recurso, endereco_entrega) values ("%s","%s","%s","%s","%s","%s","%s")' % (item[0],item[1],item[2],item[3],item[4],item[5],item[6]))
				except:
					erros += 1
			for item in itens_licitacao:
				try:
					if len(item) == 12:
						cursor.execute('INSERT INTO contratos_governo_federal.licitacao_itens (uasg, modalidade_licitacao, numero_aviso, numero_licitacao, numero_item, codigo_material_servico, item_sustentavel, quantidade, unidade_medida, beneficio, valor_estimado, decreto_7174, criterio_julgamento) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11]))
					elif len(item) == 11:
						cursor.execute('INSERT INTO contratos_governo_federal.licitacao_itens (uasg, modalidade_licitacao, numero_aviso, numero_licitacao, numero_item, codigo_material_servico, quantidade, unidade_medida, beneficio, valor_estimado, decreto_7174, criterio_julgamento) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10]))			
				except:
					erros += 1
			for item in contratos_licitacao:
				try:
					cursor.execute('INSERT INTO contratos_governo_federal.licitacoes_contratos (identificador, uasg, modalidade_licitacao, numero_aviso, codigo_contrato, licitacao_associada, origem, numero, objeto, numero_processo, cpf_contratada, data_assinatura, fundamento_legal, data_inicio, data_termino, valor_inicial) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11],item[12],item[13],item[14],item[15]))
				except:
					erros += 1
			for item in aditivos:
				try:
					cursor.execute('INSERT INTO contratos_governo_federal.licitacoes_aditivos (contrato, uasg, codigo, numero, modalidade, numero_termo, objeto, fundamento_legal, data_assinatura) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8]))
				except:
					erros += 1
	print('erros '+str(erros))
	print('terminei '+str(j))
	j += 500
