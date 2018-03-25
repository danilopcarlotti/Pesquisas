from common_nlp.textNormalization import textNormalization
from crawlers.common.conexao_local import cursorConexao

cursor = cursorConexao()
tn = textNormalization()

# cursor.execute('SELECT id, recorrido from stj.dados_processo;')
# metadados = cursor.fetchall()
# polo_passivo = tn.dicionario_invertido_id_texto(metadados)
# for k,v in polo_passivo.items():
# 	cursor.execute('INSERT INTO stj.indice_polo_passivo (palavra,id_processos) values ("%s","%s");' % (k,v))

# A REALIZAR
cursor.execute('SELECT id_processo, voto from stj.votos;')
metadados = cursor.fetchall()
votos = tn.dicionario_invertido_id_texto(metadados)
for k,v in votos.items():
	cursor.execute('INSERT INTO stj.indice_votos (palavra,id_processos) values ("%s","%s");' % (k,v))
