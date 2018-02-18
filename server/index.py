# http://jinja.pocoo.org/docs/2.10/templates/
# https://www.tutorialspoint.com/flask/flask_static_files.htm

from flask import *
app = Flask(__name__)

@app.route('/hello')
def hello_world():
   return "Hello from the other side"

@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/failure')
def failure():
   return render_template('failure.html')

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST' and request.form['senha'] == 'senha':
      user = request.form['name']
      return redirect(url_for('success',name = user))
   else:
      return redirect(url_for('failure'))

if __name__ == '__main__':
   app.run(debug = True)