from logging import raiseExceptions
from flask import request
from flask.helpers import url_for
from flask.templating import render_template
from flask import request
from flask import make_response
from flask import flash
from forms import UsuarioForm
from flask_mysqldb import MySQL
from app import app
from app import mysql

@app.route('/create_user/',methods=['GET','POST'])
def create_user():
    title = "Alta Usuarios"
    form = UsuarioForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        try:
            cur = mysql.connection.cursor()
            # Falta implementar crear usuario.
            # cur.execute("INSERT INTO publicaciones (titulo, descripcion) VALUES (%s,%s)", (titulo, descripcion))
            # mysql.connection.commit()
            flash(f"Usuario: {username} creado")
        except (MySQL.Error, MySQL.Warning) as e:
            flash(e)
        finally:
            cur.close()
    
    return render_template('create_user.html', title=title, form=form )


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





