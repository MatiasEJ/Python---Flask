from logging import raiseExceptions
from flask import Flask, config
from flask.helpers import url_for
from flask.templating import render_template
from flask import request
from flask import g
from flask_wtf import CSRFProtect
from werkzeug.utils import redirect
from flask_mysqldb import MySQL


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

@app.before_request
def before_request():
    # chequeo de datos de session/DBs
    g.test = 'TEST'  # GLOBAL? malapractica?


@app.after_request
def after_request(res):
    # chequeo de datos de session
    return res


from controladorLogin import *
from controladorPublicaciones import *


if __name__ == '__main__':
    csrf.init_app(app)
    app.run(port = 3000)
