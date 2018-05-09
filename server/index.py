# http://jinja.pocoo.org/docs/2.10/templates/
# https://www.tutorialspoint.com/flask/flask_static_files.htm

import csv, io, sys
from conexao import cursorConexao
from flask import *
from queries import Queries

app = Flask(__name__)


@app.route('/classificacao',methods = ['POST', 'GET'])
def classificacao():
    q = Queries()
    dados = q.query_padrao()
    session['id_p'] = dados[0][0]
    id_p = dados[0][0]
    tribunal = dados[0][1]
    texto_decisao = dados[0][2]
    return render_template('classificacao.html', texto_decisao = texto_decisao, id_p = id_p, tribunal = tribunal)

@app.route('/classificacao_texto',methods = ['POST'])
def classificacao_texto():
   if request.method == 'POST':
      id_p = session.get('id_p', None)
      classificacao = request.form['classe']
      cursor = cursorConexao()
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
      termos = request.form['query'].lower()
      q = Queries()
      return q.query_operadores(termos,tribunal='stf')
    except Exception as e:
      return e
  else:
    return 'Preencha o formulário corretamente, por favor.'

if __name__ == '__main__':
  app.secret_key = 'super secret key'
  app.config['SESSION_TYPE'] = 'filesystem'
  app.run(debug=True)