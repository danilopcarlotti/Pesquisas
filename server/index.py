# http://jinja.pocoo.org/docs/2.10/templates/
# https://www.tutorialspoint.com/flask/flask_static_files.htm

import csv, io, random, sys
from conexao import cursorConexao
from flask import *
from queries import Queries

app = Flask(__name__)
random.seed()


@app.route('/classificacao',methods = ['POST', 'GET'])
def classificacao():
    q = Queries()
    resultado = None
    while not resultado:
      id_aleatorio = random.randrange(1324911,5324911)
      query_txt = 'SELECT id, tribunal, texto_decisao from jurisprudencia_2_inst.jurisprudencia_2_inst where lower(texto_decisao) like "%saúde%" and classificacao is null and id = "{}";'.format(str(id_aleatorio))
      # id_aleatorio = random.randrange(19803,321358) # ID ALEATÓRIO STF
      # QUERY STF
      # query_txt = 'SELECT id, texto_decisao from stf.decisoes where lower(texto_decisao) like "%saúde%" and classificacao is null and id = "{}";'.format(str(id_aleatorio))
      # id_aleatorio = random.randrange(448,299891) # ID ALEATÓRIO STj
      # QUERY STJ
      # query_txt = 'SELECT id, voto from stj.votos where lower(voto) like "%saúde%" and classificacao is null and id = "{}";'.format(str(id_aleatorio))
      dados = q.query_padrao(query_text=query_txt)
      if dados:
        resultado = 1
        session['id_p'] = dados[0][0]
        id_p = dados[0][0]
        # 2ª INSTÂNCIA
        tribunal = dados[0][1]
        texto_decisao = dados[0][2].replace('\n', '</p>\n<p>')
        # STF
        # tribunal = 'STF'
        # texto_decisao = dados[0][1].replace('\n', '</p>\n<p>')
        # STj
        # tribunal = 'STj'
        # texto_decisao = dados[0][1].replace('\n', '</p>\n<p>')
    return render_template('classificacao.html', texto_decisao = texto_decisao, id_p = id_p, tribunal = tribunal)

@app.route('/classificacao_texto',methods = ['POST'])
def classificacao_texto():
   if request.method == 'POST':
      id_p = session.get('id_p', None)
      classificacao = request.form['classe']
      cursor = cursorConexao()
      # UṔDATE STF
      # cursor.execute('UPDATE stf.decisoes set classificacao = "%s" where id = "%s"' % (classificacao, id_p))
      # UPDATE STJ
      # cursor.execute('UPDATE stj.votos set classificacao = "%s" where id = "%s"' % (classificacao, id_p))
      # UPDATE 2ª INSTÂNCIA
      cursor.execute('UPDATE jurisprudencia_2_inst.jurisprudencia_2_inst set classificacao = "%s" where id = "%s"' % (classificacao, id_p))
      return redirect(url_for('classificacao'))
      # return render_template('classificacao_texto.html', classe = classificacao, id_p = id_p)
   else:
      return redirect(url_for('failure'))

@app.route('/index',methods = ['POST', 'GET'])
def index():
   if request.method == 'POST' and request.form['senha'] == 'senha':
      user = request.form['name']
      return redirect(url_for('index',name = user))
   else:
      return redirect(url_for('failure'))

@app.route('/')
def main_page():
  return redirect(url_for('classificacao'))
  # return render_template('login.html')

@app.route('/pesquisa', methods = ['POST', 'GET'])
def pesquisa():
   if request.method == 'POST':
      try:
         q = Queries()
         return str(q.query_tribunais(request.form['query'],tribunal='segunda_inst'))
      except Exception as e:
         return e
   else:
      return 'Preencha o formulário corretamente, por favor.'

if __name__ == '__main__':
  app.secret_key = 'super secret key'
  app.config['SESSION_TYPE'] = 'filesystem'
  app.run(debug=True)
