from textNormalization import textNormalization
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from crawlers.common.conexao_local import cursorConexao

if __name__ == '__main__':
	tabela_inicial = sys.argv[1]
	tabela_final = sys.argv[2]
	cursor = cursorConexao()
	tn = textNormalization()
	cursor.execute('SELECT id, texto from %s where texto is not null;' % (tabela_inicial,))
	dados = cursor.fetchall()
	decisoes = tn.dicionario_invertido_id_texto(dados)
	for k,v in decisoes.items():
		cursor.execute('INSERT INTO %s (palavra,id_texto) values ("%s","%s");' % (tabela_final, k, v))