from common.conexao_local import cursorConexao
from common.download_path_diarios import path
import re, os, sys, time

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca
from common_nlp.parserTextoJuridico import parserTextoJuridico

re_final_am = r'(\nPROCESSO DIGITAL: |\nDe ordem d[oa]|\nDespacho proferido pel|\n\d+ - Apelação n|\nProcesso n\. (?=\d{7})|\nProcesso :(?=\d{7})|\n\d+\. PROCESSO:(?=\d{7})|\nAutos n(?=\s*?\d{7})|\n\s*?ADV:)'
re_final_ac = r'(Acórdão n|\n\d+\. Classe|\n\d+ - (?=\d{7})|\nADV:|\nProcesso: |\nProcesso (?=\d+)|\nAutos n\.º|IV - ADMINISTRATIVO)'
re_final_ce = r'(\n.*?DESPACHO DE RELATORES|\n.*?DEC\s*?ISÃO MONOCRÁT\s?ICA|\n.*?EMENTA E CONCLUSÃO|\n.*?PORTAR\s*?IA|\n.*?CONFL\s*?ITO DE JUR\s*?ISD|\n.*?EMBARGOS DE DECLARAÇÃO|\n.*?APELAÇÃO|\nD\s*?ISTR\s*?IBU\s*?IÇÃO|\n[Nn]º (?=\d\d\d\d+))'
re_final_ma = r'(\nREQUERIMENTO DE |\nPETIÇÃO N|\nHABEAS CORPUS N|\nPORTARIA-TJ|\n\d{1,3}-PROCESSO|\nACÓRDÃO N|\nProcesso [Nn]º|\nProcesso:)'
re_final_pb = r'(\nAPELAÇÃO|\nEMBARGOS DE|\nAGRAVO|\nCONFLITO NEGATIVO|\nMANDADO DE SEGUR|\nRECURSO EM SENTIDO|\nREEXAME|\nRELATOR\(A\):|\nCOMARCA D|\nProcesso:|\nAgravo de Instrumento)'
re_final_pi = r'(\nPROCESSOS N|\n\d{1,3}\.\d{1,3}\. HABEAS CORPUS|\n\d{1,3}\.\d{1,3}\. AGRAVO DE INSTRUMENTO N|\n\d{1,3}\.\d{1,3}\. REEXAME NECESSÁRIO N|\n\d{1,3}\.\d{1,3}\. APELAÇÃO|\n\d{1,3}\.\d{1,3}\. MANDADO DE SEGURANÇA|\n\d{1,3}\.\d{1,3}\. DESPACHO|\n\d{1,3}\.\d{1,3}\. EDITAL |\n\d{1,3}\.\d{1,3}\. AVISO|\n\d{1,3}\.\d{1,3}\. ATO ORDINATÓRIO|\n\d{1,3}\.\d{1,3}\. SENTENÇA|\n\d{1,3}\.\d{1,3}\. AC.RDÃO)'
re_final_rn = r'(\nAPELAÇÃO|\nEMBARGOS DE|\nAGRAVO|\nCONFLITO NEGATIVO|\nMANDADO DE SEGUR|\nEXECUÇÃO N|\nEmbargos de|\nAgravo Interno|\nMandado de Segurança|\nApelação|\nExecução|\nAção Rescisória|\nADV:|\nAgravo de Instrumento)'
re_final_ro = r'(\nOrigem:|\nMandado de Segurança|\nNúmero do Processo|\nProcesso n|\nProc\.:|\nProcesso:)'
re_final_sc = r'(\n\s*ADV:|\nProcesso\s*(?=\d{7})|\n\d*\s*\.*\s*?Recurso |\n\d*\s*\.*\s*?Ag\s*ra\s*vo |\n\d*\s*\.*\s*?Embargo|\n\d*\s*\.*\s*?Apelação |\nRecurso |\n\s*N.\s*:(?=\d{4,7}))'
re_final_stf = r'(\nHABEAS CORPUS\s*?(?=\d+)|\nAGRAVO DE INSTRUMENTO\s*?(?=\d+)|\nMANDADO DE SEGURANÇA\s*?(?=\d+)|\nRECLAMAÇÃO\s*?(?=\d.\d+)|\nRECURSO EXTRAORDINÁRIO COM AGRAVO (?=\d+)|\nRECURSO EXTRAORDINÁRIO (?=\d+)|\nAG\.REG\.|\nEMB\.DECL\. (?=\d+)|\nAÇÃO DIRETA DE INCONSTITUCIONALIDADE (?=\d+)|\nAÇÃO ORIGINÁRIA (?=\d+)|\nAÇÃO PENAL (?=\d+)|\nMEDIDA CAUTELAR NA RECLAMAÇÃO (?=\d+)|\nMEDIDA CAUTELAR NA RECLAMAÇÃO (?=\d+)|\nCUMPRIMENTO DE SENTENÇA NA AÇÃO (?=\d+)|\nEXECUÇÃO CONTRA A FAZENDA (?=\d+)|\nEXTRADIÇÃO (?=\d+)|\nRECURSO ORDINÁRIO (?=\d+)|\nSEGUNDO AG\.REG\. (?=\d+))'
re_final_stj = r'(\nMANDADO DE SEGURANÇA [Nn]º|\nRECURSO ESPECIAL [Nn]º|\nAGRAVO EM RECURSO ESPECIAL [Nn]º|\nAgInt no RECURSO ESPECIAL [Nn]º|\nAgInt no RCD na MEDIDA CAUTELAR [Nn]º|\nEDcl no AgRg no RECURSO ESPECIAL [Nn]º|\nAgRg no AGRAVO EM RECURSO ESPECIAL [Nn]º|\nAgRg no RECURSO ESPECIAL [Nn]º|\nRECURSO EM HABEAS CORPUS [Nn]º|\nHABEAS CORPUS [Nn]º)'
re_final_to = r'(\nAutos|\nAUTOS N|\nProcesso N|\n\d+- Ação:|\nAÇÃO|\nEDITAL DE CITAÇÃO|\nEDITAL DE INTIMAÇÃO|\nPROCESSO N)'
re_final_trf4 = r'(\nAPELAÇÃO CÍVEL Nº|\nAPELAÇÃO.*?REMESSA NECESSÁRIA Nº|\nAGRAVO DE INSTRUMENTO Nº|\nEMBARGOS DE DECLARAÇÃO |\nEXECUÇÃO FISCAL Nº|\nPROCEDIMENTO COMUM Nº|\nEXECUÇÃO DE SENTENÇA CONTRA FAZENDA |\nEXECUÇÃO DE TÍTULO |\nEXECUÇÃO H\s*?IPOTECÁ|\nAÇÃO PENAL Nº|\nMON\s*?ITÓR\s*?IA Nº|\nREMESSA NECESSÁRIA CÍVEL Nº|\nAPELAÇÃO.*?REEXAME NECESSÁRIO Nº)'
re_num_cnj = r'\d{7}\s*-\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1}\s*\.\s*\d{2}\s*\.\s*\d{4}'
re_num_stf_stj = r'\d.*?( -)'
re_num_trf_trt =r'\d{7}\s*?-\d{2}\s*?\.\d{4}\s*?\.\d{1}\s*?\.\d{2}\s*?\.\d{4}|\d{7}\s*?-\d{2}\s*?\.\d{4}\s*?\.\d{3}\s*?\.\d{4}|\d{15}'

diarios = {
	'ac':[r'{}(.*?){}'.format(re_final_pb,re_final_pb),re_num_cnj],
	'al':[r'\nADV:(.*?)\nADV:',re_num_cnj],
	'am':[r'{}(.*?){}'.format(re_final_am,re_final_am),re_num_cnj],
	'ap':[r'(\nDISTRIBUIÇÃO|\nN. do processo\:|\nVARA\:)(.*?)(\nDISTRIBUIÇÃO|\nN. do processo\:|\nVARA\:)',re_num_cnj],
	'ba':[r'(DIREITO (?=\d{7}-\d{2}\.)|\nIntimação)(.*?)(DIREITO (?=\d{7}-\d{2}\.)|\nIntimação)',re_num_cnj],
	'ce':[r'{}(.*?){}'.format(re_final_ce,re_final_ce),re_num_cnj],
	'df':[r'\n\d{3}\. (?=\d{4})(.*?)\d{3}\. (?=\d{4})',re_num_cnj],
	'go':[r'(\n\s*?PROTOCOLO\s*?\:|\nNR\. PROTOCOLO|\n\s*?PROCESSO\s*?\:)(.*?)(\n\s*?PROTOCOLO\s*?\:|\nNR\. PROTOCOLO|\n\s*?PROCESSO\s*?\:)',re_num_cnj],
	'ma':[r'{}(.*?){}'.format(re_final_ma,re_final_ma),re_num_cnj],
	'mg':[r'\n\d{5} - (?=\d{7})(.*?)\n\d{5} - (?=\d{7})',re_num_cnj],
	'ms':[r'\nProcesso (?=\d+)(.*?)\nProcesso (?=\d+)',re_num_cnj],
	'mt':[r'(\nProtocolo|\nIntimação)(.*?)(\nProtocolo|\nIntimação)',re_num_cnj],
	'pa':[r'\nPROCESSO:(.*?)\nPROCESSO:',re_num_cnj],
	'pb':[r'{}(.*?){}'.format(re_final_pb,re_final_pb),re_num_cnj],
	'pe':[r'(\nProtocolo|\nProcesso)(.*?)(\nProtocolo|\nProcesso)',re_num_cnj],
	'pi':[r'{}(.*?){}'.format(re_final_pi,re_final_pi),re_num_cnj],
	'pr':[r'\n\d{1,4} \. Processo[\:/](.*?)\n\d{1,4} \. Processo[\:/]',re_num_cnj],
	'rj':[r'\nProc\.(.*?)\nProc\.',re_num_cnj],
	'rn':[r'{}(.*?){}'.format(re_final_rn,re_final_rn),re_num_cnj],
	'ro':[r'{}(.*?){}'.format(re_final_ro,re_final_ro),re_num_cnj],
	'rr':[r'\n\d{3} - (?=\d{7})(.*?)\n\d{3} - (?=\d{7})',re_num_cnj],
	'rs':[r'(\nEDITAL DE|\n(?=\d{7})-|\n.*?CNJ.*?\d{5,7}-?)(.*?)(\nEDITAL DE|\n(?=\d{7})-|\n.*?CNJ.*?\d{5,7}-?)',re_num_cnj],
	'sc':[r'{}(.*?){}'.format(re_final_sc,re_final_sc),re_num_cnj],
	'se':[r'(\nNO\. PROCESSO|\nNO\. ACORDÃO|\nPROC\.\:)(.*?)(\nNO\. PROCESSO|\nNO\. ACORDÃO|\nPROC\.\:)',re_num_cnj],
	'sp':[r'(\n\s*Processo|\n\s*?PROCESSO\:|\n\s*?N. \d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}|\n\s*?\d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\nEP\-.{1,20}PG N)(.*?)(\n\s*Processo|\n\s*?PROCESSO\:|\n\s*?N. \d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}|\n\s*?\d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\nEP\-.{1,20}PG N)',re_num_cnj],
	'stf':[r'{}(.*?){}'.format(re_final_stf,re_final_stf),re_num_stf_stj],
	'stj':[r'{}(.*?){}'.format(re_final_stj,re_final_stj),re_num_stf_stj],
	'to':[r'{}(.*?){}'.format(re_final_to,re_final_to),re_num_cnj],
	'trf1':[r'{}(.*?){}'.format(re_final_trf4,re_final_trf4),re_num_trf_trt],
	'trf2':[r'{}(.*?){}'.format(re_final_trf4,re_final_trf4),re_num_trf_trt],
	'trf3':[r'{}(.*?){}'.format(re_final_trf4,re_final_trf4),re_num_trf_trt],
	'trf4':[r'{}(.*?){}'.format(re_final_trf4,re_final_trf4),re_num_trf_trt],
	'trf5':[r'(\nPROTOCOLO N|\n\d{4}\s*?\.\s*Processo)(.*?)(\nPROTOCOLO N|\n\d{4}\s*?\.\s*Processo)',re_num_trf_trt],
	'trt':[r'(\nProcesso Nº|\nPROCESSO Nº|\nProcesso RO|\nPROCESSO N\.)(.*?)(\nProcesso Nº|\nPROCESSO Nº|\nProcesso RO|\nPROCESSO N\.)',re_num_trf_trt]
	}

if __name__ == '__main__':
	cursor = cursorConexao()
	parser = parserTextoJuridico()
	classes_publicacoes = {}
	numeros_processo = {}
	tribunais = {}
	cursor.execute('SELECT id, nome from diarios.classes_publicacoes;')
	classes_pub = cursor.fetchall()
	for id_c, nome_classe in classes_pub:
		classes_publicacoes[nome_classe] = id_c
	for repositorio_diarios in os.listdir(path):
		nome_diario = repositorio_diarios.split('Diarios_')[1]
		# print(nome_diario)
		if nome_diario not in tribunais.keys():
			cursor.execute('SELECT id from diarios.tribunais where tribunal = "%s";' % (nome_diario,))
			id_tribunal = cursor.fetchall()
			if id_tribunal:
				tribunais[nome_diario] = id_tribunal[0][0]
			else:
				cursor.execute('INSERT INTO diarios.tribunais tribunal value ("%s")' % (nome_diario,))
				time.sleep(1)
				cursor.execute('SELECT id from diarios.tribunais where tribunal = "%s";' % (nome_diario,))
				id_tribunal = cursor.fetchall()[0][0]
				tribunais[nome_diario] = id_tribunal
		for repositorio_dia in os.listdir(path+'/'+repositorio_diarios):
			for arquivo in os.listdir(path+'/'+repositorio_diarios+'/'+repositorio_dia):
				if re.search(r'txt',path+'/'+repositorio_diarios+'/'+repositorio_dia+'/'+arquivo):
					diario_texto = '\n'
					for line in open(path+'/'+repositorio_diarios+'/'+repositorio_dia+'/'+arquivo,'r'):
						diario_texto += line
					publicacoes = re.findall(diarios[nome_diario][0],diario_texto,re.DOTALL)
					for texto in publicacoes:
						if len(texto[1]) > 100:
							texto = texto[1].strip().replace('\\','').replace('/','').replace('"','')
							classe_texto = parser.classifica_texto(texto)
							numero = busca(diarios[nome_diario][1],texto,ngroup=0)
							if numero not in numeros_processo.keys():
								cursor.execute('SELECT id from diarios.numeros_proc where nome = "%s";' % (numero,))
								id_numero = cursor.fetchall()
								if id_numero:
									numeros_processo[numero] = id_numero[0][0]
								else:
									cursor.execute('INSERT INTO diarios.numeros_proc numero value ("%s")' % (numero,))
									cursor.execute('SELECT id from diarios.numeros_proc where numero = "%s";' % (numero,))
									id_numero = cursor.fetchall()[0][0]
									numeros_processo[numero] = id_numero
							cursor.execute('INSERT INTO diarios.publicacoes_diarias (id_tribunal, data, caderno, id_processo, texto, id_classe) values ("%s","%s","%s","%s","%s","%s")' % (tribunais[nome_diario], repositorio_dia, arquivo, numeros_processo[numero], texto, classes_publicacoes[classe_texto]))