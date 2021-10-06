from logging import raiseExceptions
from flask import Flask, config
from flask.helpers import url_for
from flask.templating import render_template
from flask import request
from flask import g
from flask_wtf import CSRFProtect
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
from flask import make_response
from flask import session


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
mysql = MySQL(app)

csrf = CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    title = "404"
    msg = "Page not found."
    return render_template('404.html', title=title, msg=msg), 404


@app.route('/')
def index():
    title = "Home"
    banner = "Bienvenido"
    return render_template('index.html', title=title, banner=banner)

@app.route('/login', methods=['GET', 'POST'])
def login():
    title = "Login"
    desc_form = UsuarioForm(request.form)
    if request.method == 'POST' and desc_form.validate():
        username = desc_form.username.data
        success_message = f'Bienvenido {username}'
        flash(success_message)
        session['username'] = desc_form.username.data
        print(desc_form.username.data)
        print(desc_form.password.data)

    return render_template('login.html', title=title, form=desc_form)


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for("index"))

@app.before_request
def before_request():
    # chequeo de datos de session/DBs
    g.test = 'TEST'  # GLOBAL? malapractica?


@app.after_request
def after_request(res):
    # chequeo de datos de session
    return res

@app.route('/ajax-login',methods=['POST'])
def ajax_login():
    print(request.form)
    username = request.form['username']
    # Validation
    res = {'status':200,'username':username, 'id':1}
    return json.dumps(res)

from controladorUsuario import *
from controladorPublicaciones import *


if __name__ == '__main__':
    csrf.init_app(app)
    app.run(port = 3000)
