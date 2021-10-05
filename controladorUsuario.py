from logging import raiseExceptions
import MySQLdb
from flask import Flask, config
from flask import request
from flask.helpers import url_for
from flask.templating import render_template
from flask import request
from flask import make_response
from flask import session
from flask import flash
from flask import g
from flask_wtf import CSRFProtect
from werkzeug.utils import redirect
from forms import UsuarioForm
import json
from flask_mysqldb import MySQL
from app import app
from app import mysql


@app.errorhandler(404)
def page_not_found(e):
    title = "404"
    msg = "Page not found."
    return render_template('404.html', title=title, msg=msg), 404






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
    return redirect(url_for("login"))


@app.route('/usuarios/<int:id>/')
def Usuarios(name="no se encuentra",id="nada"):
    #  param = request.args.get('id','noParams')
    #  param2 =request.args.get('nombre','noparams2')
    return render_template('usuarios.html',nombre=name) 

@app.route('/cookie',methods=['GET','POST'])
def cookie():
    title = "Cookies"
    res = make_response(render_template('cookie.html',title = title))
    res.set_cookie('custom_cookie','primer cookie')
    return res


@app.route('/ajax-login',methods=['POST'])
def ajax_login():
    print(request.form)
    username = request.form['username']
    # Validation
    res = {'status':200,'username':username, 'id':1}
    return json.dumps(res)


