# http://jinja.pocoo.org/docs/2.10/templates/
# https://www.tutorialspoint.com/flask/flask_static_files.htm

from flask import *
app = Flask(__name__)

# @app.route()

@app.route('/hello')
def hello_world():
   return "Hello from the other side"

@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name

@app.route('/failure')
def failure():
   return render_template('failure.html')

@app.route('/success')
def success():
   return render_template('success.html')

@app.route('/foo', methods = ['POST', 'GET'])
def foo():
  if request.method == 'POST':
    termos = request.form['query']
    #
    return 'Ola {}'.format(termos)
  else:
    return 'Oi'

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
  app.run(debug=True, host='0.0.0.0', port=8080)