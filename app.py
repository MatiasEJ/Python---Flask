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
from wtforms.fields.core import DecimalField
from forms import LoginForm
from model.model_user import get_user, users
import forms


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
    username = ""
    publicaciones = get_all_publicaciones()
    if 'username' in session:
        username = session['username']
        app.logger.warn("LOGEADO")
        # PASAMOS LOS ERRORES POR FLASH O POR MENSAJES?
        banner = "Bienvenido "+username
        flash("logeado, bienvenido: "+session['username'])
    else:
        app.logger.warn("no LOGEADO") #AL LOG
        banner = "Bienvenido: te invitamos a logearte o registrarte en nuestra app "
        flash("no logeado")
    return render_template('index.html', username = username, title=title, banner=banner,publicaciones = publicaciones)

@app.route('/login', methods=['GET', 'POST'])
def login():
    desc_form = LoginForm()
    if request.method == 'POST' :
        username = desc_form.username.data
        session['username'] = username
        return redirect(url_for("index"))
    return render_template('login.html', form=desc_form)

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

# @app.route('/ajax-login',methods=['POST'])
# def ajax_login():
#     username = request.form['username']
#     # Validation
#     res = {'status':200,'username':username, 'id':1}
#     return json.dumps(res)

from controladorUsuario import *
from controladorPublicaciones import *


if __name__ == '__main__':
    csrf.init_app(app)
    app.run(port = 3000)
