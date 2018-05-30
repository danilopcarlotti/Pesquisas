from common_nlp.pdf_to_text import pdf_to_text
from crawlers.common.conexao_local import cursorConexao
from crawlers.common_nlp.parserTextoJuridico import parserTextoJuridico
# from diarios_base import *
import os, re

# contador = 0
# arqs_i = os.listdir('/home/danilo/Documents/Diários_trt_2017')
# tamanho = len(arqs_i)
# cont_aux = 442
# for arq in arqs_i:
# 	if cont_aux > 0:
# 		cont_aux -= 1
# 		contador += 1
# 	else:
# 		pdf_2_txt = pdf_to_text()
# 		arq_trt = open("/home/danilo/Documents/Diários_trt_2017_txt/trt{}.txt".format(str(contador)),'a',encoding="utf-8")
# 		arq_trt.write(pdf_2_txt.convert_pdfminer('/home/danilo/Documents/Diários_trt_2017/'+arq))
# 		contador += 1
# 		arq_trt.close()
# 		print(tamanho-contador)

def indicaResultado(texto, tipo):
		# Procedência ou não da ação
		# Treinado para ações trabalhistas do TRT02
		resultado = []
		if tipo == 'Recurso':
			# VETOR RESULTADO RECURSOS POSSUI 5 POSIÇÕES
			# (INTEMPESTIVO, NÃO CONHECIDO, CONHECIDO E PROVIDO, CONHECIDO E NEGADO, CONHECIDO PARCIALMENTE PROVIDO)
			resultado = [0,0,0,0,0]
			# Caso em que o resultado aparece no corpo do acórdão
			resultadoProcesso = re.findall(r'ACORDAM(.+)\.',texto, flags=re.IGNORECASE|re.DOTALL)
			if len(resultadoProcesso):
				for r in resultadoProcesso:
					if re.search(r'intempestivo',r, flags=re.IGNORECASE|re.DOTALL) != None:
						resultado[0] = 1
					else:
						if re.search(r'(NÃO CONHECER.{1,30}DO RECURSO)|(RECURSO NÃO CONHECIDO)|RECURSO DESPROVIDO',r, flags=re.IGNORECASE|re.DOTALL) != None:
							resultado[1] = 1
						elif re.search(r'CONHECER.{1,30}[D]?O[S]? RECURSO[S]?',r, flags=re.IGNORECASE|re.DOTALL) != None:
							if re.search(r'DAR PROVIMENTO', r, flags=re.IGNORECASE|re.DOTALL) != None:
								resultado[2] = 1
							elif re.search(r'NEGAR PROVIMENTO', r, flags=re.IGNORECASE|re.DOTALL) != None:
								resultado[3] = 1
						elif re.search(r'CONHECER.{1,30}E PROVER O[S]? RECURSO[S]?',r, flags=re.IGNORECASE|re.DOTALL) != None:
							resultado[2] = 1
						elif re.search(r'CONHECER.{1,30}E NEGAR[-LHES]? PROVIMENTO',r, flags=re.IGNORECASE|re.DOTALL) != None:
							resultado[3] = 1
						elif re.search(r'RECURSO PARCIALMENTE PROVIDO', r) != None:
							resultado[4] = 1
			# Caso em que o resultado aparece na ementa ou nada identificado no texto acima
			if resultado == [0,0,0,0,0]:
				if re.search(r'recurso.{1,30}intempestivo',texto, flags=re.IGNORECASE|re.DOTALL) != None:
					resultado[0] = 1
				else:
					if re.search(r'(NÃO CONHECER.{1,30}DO RECURSO)|(RECURSO NÃO CONHECIDO)|RECURSO DESPROVIDO|\.\s*?IMPROCEDÊNCIA\.',texto, flags=re.IGNORECASE|re.DOTALL) != None:
						resultado[1] = 1
					else:
						conhecer = re.search(r'CONHECER [D]?O[S]? RECURSO[S]?(.*?)\.',texto, flags=re.IGNORECASE|re.DOTALL)
						conhecer_1 = re.search(r'RECURSO CONHECIDO(.*?)\.',texto, flags=re.IGNORECASE|re.DOTALL)
						if conhecer and conhecer.group(1) != None:
							if re.search(r'(DAR PROVIMENTO)|( PROVIDO)', conhecer.group(1)) != None:
								resultado[2] = 1
							elif re.search(r'(NEGAR PROVIMENTO)|( DESPROVIDO)', conhecer.group(1)) != None:
								resultado[3] = 1
						elif conhecer_1 and conhecer_1.group(1) != None:
							if re.search(r'(DAR PROVIMENTO)|( PROVIDO)', conhecer_1.group(1)) != None:
								resultado[2] = 1
							elif re.search(r'(NEGAR PROVIMENTO)|( DESPROVIDO)', conhecer_1.group(1)) != None:
								resultado[3] = 1
						elif re.search(r'RECURSO PARCIALMENTE PROVIDO', texto) != None:
							resultado[4] = 1
		return resultado

arquivo = open('acordaos_tjsc_justica_gratuita.txt','w')
cursor = cursorConexao()
cursor.execute('SELECT numero, texto_decisao FROM jurisprudencia_2_inst.jurisprudencia_2_inst_sc where procedencia != "[0, 0, 0, 0, 0]";')
dados = cursor.fetchall()
for id_p, texto in dados:
	arquivo.write('\n\nNúmero do processo: ')
	arquivo.write(id_p)
	arquivo.write('\n\nTexto do acórdão:\n\n')
	arquivo.write(texto)
	# procedente = indicaResultado(texto, 'Recurso')
	# cursor.execute('UPDATE jurisprudencia_2_inst.jurisprudencia_2_inst_sc set procedencia = "%s" where id = "%s";' % (procedente,id_p))