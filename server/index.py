# http://jinja.pocoo.org/docs/2.10/templates/
# https://www.tutorialspoint.com/flask/flask_static_files.htm

import csv
import io

from flask import *

from conexao import cursorConexao

app = Flask(__name__)

@app.route('/pesquisa', methods = ['POST', 'GET'])
def foo():
  if request.method == 'POST':
    try:
      termos = request.form['query'].lower()
      cursor = cursorConexao()
      cursor.execute('SELECT texto_decisao FROM stf.decisoes where lower(texto_decisao) like "%{}%" limit 10;'.format(termos))
      dados = cursor.fetchall()
      si = io.StringIO()
      cw = csv.writer(si)
      cw.writerows([['Texto decisão']])
      cw.writerows(dados)
      output = make_response(si.getvalue())
      output.headers["Content-Disposition"] = "attachment; filename=relatorio_insper_cnj.csv"
      output.headers["Content-type"] = "text/csv"
      return output
    except Exception as e:
      return e
  else:
    return 'Preencha o formulário corretamente, por favor.'

@app.route('/')
def main_page():
  return render_template('login.html')

@app.route('/index',methods = ['POST', 'GET'])
def index():
   if request.method == 'POST' and request.form['senha'] == 'senha':
      user = request.form['name']
      return redirect(url_for('index',name = user))
   else:
      return redirect(url_for('failure'))

if __name__ == '__main__':
  app.run(debug=True)