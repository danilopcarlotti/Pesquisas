from crawlers.common.conexao_local import cursorConexao
import re

ids_stj = []
for line in open('rascunhos.txt','r'):
	if line.replace('\n','') not in ids_stj:
		ids_stj.append(line.replace('\n',''))
cursor = cursorConexao()


