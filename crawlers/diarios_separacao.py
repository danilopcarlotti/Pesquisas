import re, os, sys, time

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca
from common_nlp.parserTextoJuridico import parserTextoJuridico

re_final_ac = '\n\s*?Acórdão n|\n\d+\. Classe|\n\s*?Classe|\n\d+\. CLASSE|\n\s*?CLASSE|\n\d+ - (?=\d{7})|\n\s*?ADV\:|\n\s*?Processo: |\n\s*?Processo (?=\d+)|\n\s*?Autos n\.°'
re_final_am = '\n.{0,15}PROCESSO DIGITAL\:|\n.{0,15}De ordem d[oa]|\n.{0,15}Despacho proferido pel|\n.{0,15}Apelação n|\n.{0,15}Processo n\.|\n.{0,15}Processo\s*?\:|\n.{0,15}PROCESSO\:|\n.{0,15}Autos n(?=\n\d{7})|\n.{0,15}ADV\:|\n.{0,15}Apelação|\n.{0,15}Agravo|\n.{0,15}Recurso'
re_final_ce = '\n\s*?PROCESSO|\n\s*?Processo|\n\s*?DECISÃO MONOCRÁTICA|\n\s*?\d{1,5}\)|\s*D\s*ISTR\s*IBU\s*IÇÃO|\n\s° (?=\d\d\d\d+)|\n\s*?ADV\:|(\n\s*?\d{4,8}\-\d\d\.\d{4}\.\d\.\d\d\.\d{4})|(\n\s*?\d+\)\s*?\d{4,8}\-\d\d\.\d{4}\.\d\.\d\d\.\d{4})'
re_final_ma = '\n\s*?REQUERIMENTO DE |\nPETIÇÃO N|\nHABEAS CORPUS N|\nPORTARIA-TJ|\n\d{1,3}-PROCESSO|\nACÓRDÃO N|\nProcesso [Nn]°|\nProcesso\:'
re_final_pa = '\n\s*?PROCESSO\:|\n\s*?Processo\:'
re_final_pb = '\n\s*?APELAÇÃO|\n\s*?HABEAS|\n\s*?MANDADO|\n\s*?EMBARGOS|\n\s*?AGRAVO|\n\s*?CONFLITO NEGATIVO|\n\s*?RECURSO|\n\s*?REEXAME|\n\s*?RELATOR\(A\)\:|\n\s*?COMARCA|\n\s*?Processo|\n\s*?\d+\s*?Processo|\n\s*?Agravo de Instrumento'
re_final_pi = '\n\s*?PROCESSOS [Nn]|\n\s*?HABEAS CORPUS [Nn]|\n\s*?AGRAVO DE INSTRUMENTO [Nn]|\n\s*?REEXAME NECESSÁRIO [Nn]|\n\s*?APELAÇÃO|\n\s*?MANDADO DE SEGURANÇA [Nn]|\n\s*?DESPACHO|\n\s*?EDITAL |\n\s*?AVISO|\n\s*?ATO ORDINATÓRIO|\n\s*?SENTENÇA|\n\s*?Processos [Nn]|\n\s*?Habeas Corpus [Nn]|\n\s*?Agravo De Instrumento [Nn]|\n\s*?Reexame Necessário [Nn]|\n\s*?Apelação|\n\s*?Mandado de Segurança [Nn]|\n\s*?Despacho|\n\s*?Edital|\n\s*?Aviso|\n\s*?Ato Ordinatório|\n\s*?Sentença|\n\s*?Ref\. Processo|\n\s*?PROCESSO [Nn]|\n\s*?\d*\-*\s*?Processo [Nn]|\n\s*?\d+\.\s(\d{4})'
re_final_rn = '\n\s*?APELAÇÃO.*?N\.*°|\n\s*?EMBARGOS DE.*?N\.*°|\n\s*?AGRAVO.*?N\.*°|\n\s*?CONFLITO NEGATIVO.*?N\.*°|\n\s*?MANDADO DE SEGUR.*?N\.*°|\n\s*?EXECUÇÃO.*?N\.*°|\n\d*\s*?\-*\s*?Embargos de|\n\d*\s*?\-*\s*?Agravo Interno|\n\d*\s*?\-*\s*?Mandado de Segurança|\n\d*\s*?\-*\s*?Apelação|\n\d*\s*?\-*\s*?Execução|\n\d*\s*?\-*\s*?Ação Rescisória|\n\s*?ADV\:|\n\d*\s*?\-*\s*?Agravo de Instrumento'
re_final_ro = '\nOrigem\:|\nMandado de Segurança|\nNúmero do Processo|\nProcesso n|\nProc\.\:|\nProcesso\:'
re_final_sc = '\n\s*ADV\s*?\:|\nProcesso|\n\d*\s*\.*Recurso |\n\d*\s*\.*Ag\s*ra\s*vo |\n\d*\s*\.*Embargo|\n\d*\s*\.*Apelação |\n\d*\s*\.*Recurso |\n\s*N\.*°*|\n\s*\d+\s*?\-\s*?N\.*°*'
re_final_stf = '\nHABEAS CORPUS\n(?=\d+)|\nAGRAVO DE INSTRUMENTO\n(?=\d+)|\nMANDADO DE SEGURANÇA\n(?=\d+)|\nRECLAMAÇÃO\n(?=\d.\d+)|\nRECURSO EXTRAORDINÁRIO COM AGRAVO (?=\d+)|\nRECURSO EXTRAORDINÁRIO (?=\d+)|\nAG\.REG\.|\nEMB\.DECL\. (?=\d+)|\nAÇÃO DIRETA DE INCONSTITUCIONALIDADE (?=\d+)|\nAÇÃO ORIGINÁRIA (?=\d+)|\nAÇÃO PENAL (?=\d+)|\nMEDIDA CAUTELAR NA RECLAMAÇÃO (?=\d+)|\nMEDIDA CAUTELAR NA RECLAMAÇÃO (?=\d+)|\nCUMPRIMENTO DE SENTENÇA NA AÇÃO (?=\d+)|\nEXECUÇÃO CONTRA A FAZENDA (?=\d+)|\nEXTRADIÇÃO (?=\d+)|\nRECURSO ORDINÁRIO (?=\d+)|\nSEGUNDO AG\.REG\. (?=\d+)'
re_final_stj = '\nMANDADO DE SEGURANÇA [Nn]°|\nRECURSO ESPECIAL [Nn]°|\nAGRAVO EM RECURSO ESPECIAL [Nn]°|\nAgInt no RECURSO ESPECIAL [Nn]°|\nAgInt no RCD na MEDIDA CAUTELAR [Nn]°|\nEDcl no AgRg no RECURSO ESPECIAL [Nn]°|\nAgRg no AGRAVO EM RECURSO ESPECIAL [Nn]°|\nAgRg no RECURSO ESPECIAL [Nn]°|\nRECURSO EM HABEAS CORPUS [Nn]°|\nHABEAS CORPUS [Nn]°'
re_final_to = '\n\s*?Autos n|\n\s*?AUTOS N|\n\s*?Processo N|\n\s*?EDITAL DE CITAÇÃO|\n\s*?EDITAL DE INTIMAÇÃO|\n\s*?PROCESSO N|\n\s*?PROTOCOLO|\n\s*?\d{1,4}\s*?\-\s*?Recurso|\n\s*?ORIGEM\:'
re_final_trf1 = '\n\s*?Numera..o .nica\:|\n\s*?PODER JUDICI.RIO|\n\s*?(\d{4,8}\s*\-*\.*\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1}\s*\.\s*\d{2}\s*\.\s*\d{4})|\n\s*?AGRAVO\n\s*?EMBARGOS|\n\s*?MANDADO|\n\s*?EXECUÇÃO|\n\s*?PROCEDIMENTO|\n\s*?AÇÃO|\n\s*?REMESSA|\n\s*?APELAÇÃO|\n\s*?EDITAL'
re_final_trf3 = r'\n\s*?\d{4,8}\s*\-\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1,3}\s*\.\s*\d{4}|\n\s*?PROCESSO|\n\s*?\d{4,8}\.\d{2}\.\d{2}\.\d{6}\-\d|\n\s*?\d{5}\s|\n\s*?PROC\.|\n\s*?Processo n|\n\s*?\d{2}\.\d{7}\-\d|\n\s*?AGRAVO|\n\s*?EMBARGOS|\n\s*?MANDADO|\n\s*?EXECUÇÃO|\n\s*?PROCEDIMENTO|\n\s*?AÇÃO|\n\s*?REMESSA|\n\s*?APELAÇÃO\s*?CÍVEL|\n\s*?APELAÇÃO\s*?REMESSA|\n\s*?APELAÇÃO\s*?REEXAME|\n\s*?EDITAL'
re_final_trf4 = '\n\s*?AGRAVO\n\s*?EMBARGOS|\n\s*?MANDADO|\n\s*?EXECUÇÃO|\n\s*?PROCEDIMENTO|\n\s*?AÇÃO|\n\s*?REMESSA|\n\s*?APELAÇÃO|\n\s*?EDITAL|\n\s*?\d{7}\s'
re_final_trf5 = '\n\s*?AC \-|\n\s*?AGTR|\n\s*?REOAC|\n\s*?APELREEX|\n\s*?AGIVP|\s*?PROTOCOLO N|\s*?\d{4}\s*?\.\s*Processo'
re_num_cnj = r'\d{4,8}\s*\-*\.*\s*\d{2}\s*\.*\s*\d{4}\s*\.*\s*\d{1}\s*\.*\s*\d{2}\s*\.*\s*\d{4}'
re_num_stf_stj = r'\d.*?( -)'
re_num_trf_trt =r'\d{4}\.\d{2}\.\d{2}\.\d{6}\-\d|\d{7}\s*?-\d{2}\s*?\.\d{4}\s*?\.\d{1}\s*?\.\d{2}\s*?\.\d{4}|\d{7}\s*?-\d{2}\s*?\.\d{4}\s*?\.\d{3}\s*?\.\d{4}|\d{15}|\d{3,5}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}'

dicionario_separacao_diarios = {
	'ac':[r'{}'.format(re_final_ac,),re_num_cnj],
	'al':[r'\n\s*?ADV\s*?\:|\n\s*?Macei.*?\n',re_num_cnj],
	'am':[r'{}'.format(re_final_am,),re_num_cnj],
	'ap':[r'\nDISTRIBUIÇÃO|\nN. do processo\:|\nVARA\:',re_num_cnj],
	'ba':[r'DIREITO (?=\d{7}-\d{2}\.)|\nIntimação',re_num_cnj],
	'ce':[r'{}'.format(re_final_ce,),r'\d{4,8}\s*-\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1}\s*\.\s*\d{2}\s*\.\s*\d{4}'],
	'df':[r'\n\d{1,4}\. (?=\d{4})|\nNum Processo|\nN. |\n\s*?Distribuição',r'\d{4,8}\s*-?\.?\s*\d{2}\s*\.?\s*\d{4}\s*\.?\s*\d{1}\s*\.?\s*\d{2}\s*\.?\s*\d{4}|\d{4}\.*\s*\d{2}\.*\s*\d\.*\s*\d{6}\-*\s*\d'],
	'go':[r'\n\s*?PROTOCOLO\s*?\:|\n\s*?NR\.|\n\s*?PROCESSO\s*?\:|\n\s*?\d+\s*?\-\s*?Processo n|\n\s*?Proc\.',re_num_cnj],
	'ma':[r'{}'.format(re_final_ma,),re_num_cnj],
	'mg':[r'\n\d{5} - (?=\d{7}',re_num_cnj],
	'ms':[r'\nJUÍZO DE DIREITO DA|\n\s*?Agravo de Instrumento|\n\s*?Apelação|\n\s*?Habeas Corpus|\n\s*?Comarca de|\n\s*?Revisão Criminal|\n\s*?Mandado de Segurança|\n\s*?Recurso Em Sentido Estrito|\n\s*?Embargos|\n\s*?Exceção|\n\s*?Reexame',re_num_cnj],
	'mt':[r'\n\s*?Protocolo|\n\s*?Intimação|\n\s*?Cod\.\s*?Proc\.|\n\s*?Processo',r'\d{4,8}\s*-*\.*\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1}\s*\.\s*\d{2}\s*\.\s*\d{4}|\d{4,8}\s*-*\.*\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1,3}\s*\.\s*\d{2,4}'],
	'pa':[r'{}'.format(re_final_pa,),re_num_cnj],
	'pb':[r'{}'.format(re_final_pb,),r'\d{4,8}\s*-*\.*\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1}\s*\.\s*\d{2}\s*\.\s*\d{4}|\d{4,8}\s*-*\.*\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1,3}\s*\.\s*\d{2,4}|\d{17}'],
	'pe':[r'\n\s*?Protocolo|\n\s*?Processo N',re_num_cnj],
	'pi':[r'{}'.format(re_final_pi,),r'\d{4,8}\s*-*\.*\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1}\s*\.\s*\d{2}\s*\.\s*\d{4}|\d{4,8}\s*-*\.*\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1,3}\s*\.\s*\d{2,4}|\d{4}\.\d{4,6}\.\d{6,8}\-\d'],
	'pr':[r'\n\d{1,4} \. Processo[\:/]|\n\d+\.\s',re_num_cnj],
	'rj':[r'\nProc\.',re_num_cnj],
	'rn':[r'{}'.format(re_final_rn,),r'\d{4,8}\s*-*\.*\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1}\s*\.\s*\d{2}\s*\.\s*\d{4}|\d{4}\.\d{6}\-\d'],
	'ro':[r'{}'.format(re_final_ro,),re_num_cnj],
	'rr':[r'\n\d{3}\s*?\-',re_num_cnj],
	'rs':[r'\nEDITAL DE|\n(?=\d{7})-|\n\d+\s*?\-\s*?.*?CNJ\s*?\:',re_num_cnj],
	'sc':[r'{}'.format(re_final_sc,),re_num_cnj],
	'se':[r'\n\s*?NO\. PROCESSO|\n\s*?NO\. ACORDÃO|\n\s*?PROC\.\:',r'\d{4,8}\s*-*\.*\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1}\s*\.\s*\d{2}\s*\.\s*\d{4}|\d{10,12}'],
	'sp':[r'\n\s*?Processo |\n\s*?PROCESSO\:|\n\s*?N\.*[º°](?! ORDEM)|\n\s*?\d+\s*?\-\s',r'\n\s*?\d{4,8}\s*-*\.*\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1}\s*\.\s*\d{2}\s*\.\s*\d{4}|\n\s*?\d{3}\s*\-*\.*\s*\d{2}'],
	'stf':[r'{}'.format(re_final_stf,),re_num_stf_stj],
	'stj':[r'{}'.format(re_final_stj,),re_num_stf_stj],
	'to':[r'{}'.format(re_final_to,),r'\d{4,8}\s*-*\.*\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1}\s*\.\s*\d{2}\s*\.*\-*\s*\d{4}|\d{4}\.\d{4}\.\d{4}\-*\.*\d|\d{4}\/\d{2}'],
	'trf1':[r'{}'.format(re_final_trf1,),re_num_trf_trt],
	'trf2':[r'{}'.format(re_final_trf4,),re_num_trf_trt],
	'trf3':[r'{}'.format(re_final_trf3,),re_num_trf_trt],
	'trf4':[r'{}'.format(re_final_trf4,),re_num_trf_trt],
	'trf5':[r'{}'.format(re_final_trf5,),re_num_trf_trt],
	'trt':[r'\s*?Processo N\.*°|\s*?Processo RO|\s*?PROCESSO N\.',re_num_trf_trt]
}

def encontra_publicacoes(tribunal, texto):
	return re.split(dicionario_separacao_diarios[tribunal][0],texto)

def encontra_numero(tribunal, texto):
	return busca(dicionario_separacao_diarios[tribunal][1],texto,ngroup=0).replace('\n','')