# from common.conexao_local import cursorConexao
# from common.download_path_diarios import path
import re, os, sys, time

sys.path.append(os.path.dirname(os.getcwd()))
from Pesquisas.common_nlp.parse_texto import busca
from Pesquisas.common_nlp.parserTextoJuridico import parserTextoJuridico

re_final_ac = '\nAcórdão n|\n\d+\. Classe|\n\d+ - (?=\d{7})|\nADV\:|\nProcesso: |\nProcesso (?=\d+)|\nAutos n\.º'
re_final_am = '\nPROCESSO DIGITAL\:|\nDe ordem d[oa]|\nDespacho proferido pel|\n\d+ - Apelação n|\nProcesso n\. (?=\d{7})|\nProcesso \:(?=\d{7})|\n\d+\. PROCESSO\:(?=\d{7})|\nAutos n(?=\n\d{7})|\n\nADV\:'
re_final_ce = '\n.*?DESPACHO DE RELATORES|\n.*?DEC\nISÃO MONOCRÁT\s?ICA|\n.*?EMENTA E CONCLUSÃO|\n.*?PORTAR\nIA|\n.*?CONFL\nITO DE JUR\nISD|\n.*?EMBARGOS DE DECLARAÇÃO|\n.*?APELAÇÃO|\nD\nISTR\nIBU\nIÇÃO|\n[Nn]º (?=\d\d\d\d+)'
re_final_ma = '\nREQUERIMENTO DE |\nPETIÇÃO N|\nHABEAS CORPUS N|\nPORTARIA-TJ|\n\d{1,3}-PROCESSO|\nACÓRDÃO N|\nProcesso [Nn]º|\nProcesso\:'
re_final_pb = '\nAPELAÇÃO|\nEMBARGOS DE|\nAGRAVO|\nCONFLITO NEGATIVO|\nMANDADO DE SEGUR|\nRECURSO EM SENTIDO|\nREEXAME|\nRELATOR\(A\)\:|\nCOMARCA D|\nProcesso\:|\nAgravo de Instrumento'
re_final_pi = '\nPROCESSOS N|\n\d{1,3}\.\d{1,3}\. HABEAS CORPUS|\n\d{1,3}\.\d{1,3}\. AGRAVO DE INSTRUMENTO N|\n\d{1,3}\.\d{1,3}\. REEXAME NECESSÁRIO N|\n\d{1,3}\.\d{1,3}\. APELAÇÃO|\n\d{1,3}\.\d{1,3}\. MANDADO DE SEGURANÇA|\n\d{1,3}\.\d{1,3}\. DESPACHO|\n\d{1,3}\.\d{1,3}\. EDITAL |\n\d{1,3}\.\d{1,3}\. AVISO|\n\d{1,3}\.\d{1,3}\. ATO ORDINATÓRIO|\n\d{1,3}\.\d{1,3}\. SENTENÇA|\n\d{1,3}\.\d{1,3}\. AC.RDÃO'
re_final_rn = '\nAPELAÇÃO|\nEMBARGOS DE|\nAGRAVO|\nCONFLITO NEGATIVO|\nMANDADO DE SEGUR|\nEXECUÇÃO N|\nEmbargos de|\nAgravo Interno|\nMandado de Segurança|\nApelação|\nExecução|\nAção Rescisória|\nADV\:|\nAgravo de Instrumento'
re_final_ro = '\nOrigem\:|\nMandado de Segurança|\nNúmero do Processo|\nProcesso n|\nProc\.\:|\nProcesso\:'
re_final_sc = '\n\s*ADV\:|\nProcesso\s*(?=\d{7})|\n\d*\s*\.*\nRecurso |\n\d*\s*\.*\nAg\s*ra\s*vo |\n\d*\s*\.*\nEmbargo|\n\d*\s*\.*\nApelação |\nRecurso |\n\s*N.\s*\:(?=\d{4,7}'
re_final_stf = '\nHABEAS CORPUS\n(?=\d+)|\nAGRAVO DE INSTRUMENTO\n(?=\d+)|\nMANDADO DE SEGURANÇA\n(?=\d+)|\nRECLAMAÇÃO\n(?=\d.\d+)|\nRECURSO EXTRAORDINÁRIO COM AGRAVO (?=\d+)|\nRECURSO EXTRAORDINÁRIO (?=\d+)|\nAG\.REG\.|\nEMB\.DECL\. (?=\d+)|\nAÇÃO DIRETA DE INCONSTITUCIONALIDADE (?=\d+)|\nAÇÃO ORIGINÁRIA (?=\d+)|\nAÇÃO PENAL (?=\d+)|\nMEDIDA CAUTELAR NA RECLAMAÇÃO (?=\d+)|\nMEDIDA CAUTELAR NA RECLAMAÇÃO (?=\d+)|\nCUMPRIMENTO DE SENTENÇA NA AÇÃO (?=\d+)|\nEXECUÇÃO CONTRA A FAZENDA (?=\d+)|\nEXTRADIÇÃO (?=\d+)|\nRECURSO ORDINÁRIO (?=\d+)|\nSEGUNDO AG\.REG\. (?=\d+)'
re_final_stj = '\nMANDADO DE SEGURANÇA [Nn]º|\nRECURSO ESPECIAL [Nn]º|\nAGRAVO EM RECURSO ESPECIAL [Nn]º|\nAgInt no RECURSO ESPECIAL [Nn]º|\nAgInt no RCD na MEDIDA CAUTELAR [Nn]º|\nEDcl no AgRg no RECURSO ESPECIAL [Nn]º|\nAgRg no AGRAVO EM RECURSO ESPECIAL [Nn]º|\nAgRg no RECURSO ESPECIAL [Nn]º|\nRECURSO EM HABEAS CORPUS [Nn]º|\nHABEAS CORPUS [Nn]º'
re_final_to = '\nAutos n.|\nAUTOS N.|\nProcesso N.|\nEDITAL DE CITAÇÃO|\nEDITAL DE INTIMAÇÃO|\nPROCESSO N.|\nPROTOCOLO|\d{1,4} - Recurso'
re_final_trf4 = '\nAPELAÇÃO CÍVEL Nº|\nAPELAÇÃO.*?REMESSA NECESSÁRIA Nº|\nAGRAVO DE INSTRUMENTO Nº|\nEMBARGOS DE DECLARAÇÃO |\nEXECUÇÃO FISCAL Nº|\nPROCEDIMENTO COMUM Nº|\nEXECUÇÃO DE SENTENÇA CONTRA FAZENDA |\nEXECUÇÃO DE TÍTULO |\nEXECUÇÃO H\nIPOTECÁ|\nAÇÃO PENAL Nº|\nMON\nITÓR\nIA Nº|\nREMESSA NECESSÁRIA CÍVEL Nº|\nAPELAÇÃO.*?REEXAME NECESSÁRIO Nº'
re_num_cnj = r'\d{6,7}\s*-\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1}\s*\.\s*\d{2}\s*\.\s*\d{4}'
re_num_stf_stj = r'\d.*?( -)'
re_num_trf_trt =r'\d{7}\s*?-\d{2}\s*?\.\d{4}\s*?\.\d{1}\s*?\.\d{2}\s*?\.\d{4}|\d{7}\s*?-\d{2}\s*?\.\d{4}\s*?\.\d{3}\s*?\.\d{4}|\d{15}'

diarios = {
	'ac':[r'{}'.format(re_final_ac,),re_num_cnj],
	'al':[r'\nADV\:',re_num_cnj],
	'am':[r'{}'.format(re_final_am,),re_num_cnj],
	'ap':[r'\nDISTRIBUIÇÃO|\nN. do processo\:|\nVARA\:',re_num_cnj],
	'ba':[r'DIREITO (?=\d{7}-\d{2}\.)|\nIntimação',re_num_cnj],
	'ce':[r'{}'.format(re_final_ce,),re_num_cnj],
	'df':[r'\n\d{1,3}\. (?=\d{4})',re_num_cnj],
	'go':[r'\nPROTOCOLO\n\:|\nNR\. PROTOCOLO|\nPROCESSO\s*?\:',re_num_cnj],
	'ma':[r'{}'.format(re_final_ma,),re_num_cnj],
	'mg':[r'\n\d{5} - (?=\d{7}',re_num_cnj],
	'ms':[r'\nJUÍZO DE DIREITO DA ',re_num_cnj],
	'mt':[r'\nProtocolo|\nIntimação',re_num_cnj],
	'pa':[r'\nPROCESSO\:',re_num_cnj],
	'pb':[r'{}'.format(re_final_pb,),re_num_cnj],
	'pe':[r'\nProtocolo|\nProcesso',re_num_cnj],
	'pi':[r'{}'.format(re_final_pi,),re_num_cnj],
	'pr':[r'\n\d{1,4} \. Processo[\:/]',re_num_cnj],
	'rj':[r'\nProc\.',re_num_cnj],
	'rn':[r'{}'.format(re_final_rn,),re_num_cnj],
	'ro':[r'{}'.format(re_final_ro,),re_num_cnj],
	'rr':[r'\n\d{3} - (?=\d{7}',re_num_cnj],
	# 'rs':[r'\nEDITAL DE|\n(?=\d{7})-|\n.*?CNJ.*?\d{5,7}-?',re_num_cnj],
	'sc':[r'{}'.format(re_final_sc,),re_num_cnj],
	'se':[r'\nNO\. PROCESSO|\nNO\. ACORDÃO|\s*?PROC\.\:',re_num_cnj],
	'sp':[r'\s*?\s*Processo|\s*?\s*?PROCESSO\:|\s*?\s*?N. \d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}|\s*?\s*?\d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\s*?EP\-.{1,20}PG N',re_num_cnj],
	'stf':[r'{}'.format(re_final_stf,),re_num_stf_stj],
	'stj':[r'{}'.format(re_final_stj,),re_num_stf_stj],
	'to':[r'{}'.format(re_final_to,),re_num_cnj],
	# 'trf1':[r'{}'.format(re_final_trf4,),re_num_trf_trt],
	# 'trf2':[r'{}'.format(re_final_trf4,),re_num_trf_trt],
	# 'trf3':[r'{}'.format(re_final_trf4,),re_num_trf_trt],
	# 'trf4':[r'{}'.format(re_final_trf4,),re_num_trf_trt],
	# 'trf5':[r'\s*?PROTOCOLO N|\s*?\d{4}\s*?\.\s*Processo',re_num_trf_trt],
	'trt':[r'\s*?Processo Nº|\s*?PROCESSO Nº|\s*?Processo RO|\s*?PROCESSO N\.',re_num_trf_trt]
	}

def encontra_publicacoes(tribunal, texto):
	return re.split(diarios[tribunal][0],texto)

def encontra_numero(tribunal, texto):
	return busca(diarios[tribunal][1],texto,ngroup=0)

def encontra_data(texto):
	data = re.search(r'\d{2}/\d{2}/\d{4}|\d{2}-\d{2}-\d{4}',texto)
	if data:
		return data.group(0)
	else:
		return ''

# if __name__ == '__main__':
# 	cursor = cursorConexao()
# 	parser = parserTextoJuridico()
# 	classes_publicacoes = {}
# 	numeros_processo = {}
# 	tribunais = {}
# 	cursor.execute('SELECT id, nome from diarios.classes_publicacoes;')
# 	classes_pub = cursor.fetchall()
# 	for id_c, nome_classe in classes_pub:
# 		classes_publicacoes[nome_classe] = id_c
# 	for repositorio_diarios in os.listdir(path):
# 		nome_diario = repositorio_diarios.split('Diarios_')[1]
# 		# print(nome_diario)
# 		if nome_diario not in tribunais.keys():
# 			cursor.execute('SELECT id from diarios.tribunais where tribunal = "%s";' % (nome_diario,))
# 			id_tribunal = cursor.fetchall()
# 			if id_tribunal:
# 				tribunais[nome_diario] = id_tribunal[0][0]
# 			else:
# 				cursor.execute('INSERT INTO diarios.tribunais tribunal value ("%s")' % (nome_diario,))
# 				time.sleep(1)
# 				cursor.execute('SELECT id from diarios.tribunais where tribunal = "%s";' % (nome_diario,))
# 				id_tribunal = cursor.fetchall()[0][0]
# 				tribunais[nome_diario] = id_tribunal
# 		for repositorio_dia in os.listdir(path+'/'+repositorio_diarios):
# 			for arquivo in os.listdir(path+'/'+repositorio_diarios+'/'+repositorio_dia):
# 				if re.search(r'txt',path+'/'+repositorio_diarios+'/'+repositorio_dia+'/'+arquivo):
# 					diario_texto = '\n'
# 					for line in open(path+'/'+repositorio_diarios+'/'+repositorio_dia+'/'+arquivo,'r'):
# 						diario_texto += line
# 					publicacoes = re.findall(diarios[nome_diario][0],diario_texto,re.DOTALL)
# 					for texto in publicacoes:
# 						if len(texto[1]) > 100:
# 							texto = texto[1].strip().replace('\\','').replace('/','').replace('"','')
# 							classe_texto = parser.classifica_texto(texto)
# 							numero = busca(diarios[nome_diario][1],texto,ngroup=0)
# 							if numero not in numeros_processo.keys():
# 								cursor.execute('SELECT id from diarios.numeros_proc where nome = "%s";' % (numero,))
# 								id_numero = cursor.fetchall()
# 								if id_numero:
# 									numeros_processo[numero] = id_numero[0][0]
# 								else:
# 									cursor.execute('INSERT INTO diarios.numeros_proc numero value ("%s")' % (numero,))
# 									cursor.execute('SELECT id from diarios.numeros_proc where numero = "%s";' % (numero,))
# 									id_numero = cursor.fetchall()[0][0]
# 									numeros_processo[numero] = id_numero
# 							cursor.execute('INSERT INTO diarios.publicacoes_diarias (id_tribunal, data, caderno, id_processo, texto, id_classe) values ("%s","%s","%s","%s","%s","%s")' % (tribunais[nome_diario], repositorio_dia, arquivo, numeros_processo[numero], texto, classes_publicacoes[classe_texto]))