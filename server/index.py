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

@app.route('/index/<name>')
def index(name):
   return 'Bem vindo %s' % name

@app.route('/failure')
def failure():
   return render_template('failure.html')

@app.route('/success')
def success():
   return render_template('success.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(user)
        flask.flash('Logged in successfully.')
        next = flask.request.args.get('next')
        if not is_safe_url(next):
            return flask.abort(400)
        return flask.redirect(next or flask.url_for('success'))
    return flask.render_template('failure.html', form=form)

@app.route('/index',methods = ['POST', 'GET'])
def index():
   if request.method == 'POST' and request.form['senha'] == 'senha':
      user = request.form['name']
      return redirect(url_for('index',name = user))
   else:
      return redirect(url_for('failure'))

if __name__ == '__main__':
   app.run(debug = True)