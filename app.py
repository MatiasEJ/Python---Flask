from logging import raiseExceptions
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
import LoginForm
import PublicacionForm
import json
from flask_mysqldb import MySQL
import errorDb


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
mysql = MySQL(app)

csrf = CSRFProtect()


@app.errorhandler(404)
def page_not_found(e):
    title = "404"
    msg = "Page not found."
    return render_template('404.html', title=title, msg=msg), 404


@app.before_request
def before_request():
    # chequeo de datos de session/DBs
    g.test = 'TEST'  # GLOBAL? malapractica?


@app.after_request
def after_request(res):
    # chequeo de datos de session
    return res


@app.route('/')
def index():
    title = "Home"
    banner = "Bienvenido"
    return render_template('index.html', title=title, banner=banner)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = "Login"
    desc_form = LoginForm.LoginForm(request.form)

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


@app.route('/publicacion/', methods=['GET', 'POST'])
def altaPublicacion():
    title = "Alta Publicacion"
    desc_form = PublicacionForm.PublicacionForm(request.form)
    if request.method == 'POST' and desc_form.validate():
        titulo = desc_form.titulo.data
        descripcion = desc_form.descripcion.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO publicaciones (titulo, descripcion) VALUES (%s,%s)", (titulo, descripcion))
        mysql.connection.commit()
        flash("Publicacion creada.")
    return render_template('altaPublicacion.html', title=title, form=desc_form)


@app.route('/publicaciones', methods=['GET'])
def publicaciones():
    error = ""
    msgError = ""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM publicaciones")
        data = cur.fetchall()
    except:
        error = "Error conexion db"
        msgError = "No se pudo conectar a la base de datos."

    if len(data) == 0:
        error = "Lista Vacia"
        msgError = "No existen publicaciones del usuario."

    return render_template('publicaciones.html', error=error, msgError=msgError, publicaciones=data)


@app.route('/delete/<int:id>/', methods=['GET', 'POST'])
def delete_publicacion(id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT titulo from publicaciones where id = {id};")
    publicacion = getPublicacionById(id) 
    cur.execute(f"DELETE from publicaciones where id = {id};")
    mysql.connection.commit()
    flash(f"Publicacion: {publicacion} eliminada.")
    return redirect(url_for("publicaciones"))

@app.route('/update/<int:id>/',methods=['GET','POST'])
def update_publicacion(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        titulo = request.form['titulo']    
        descripcion = request.form['descripcion']    
        cur.execute("""
        UPDATE publicaciones 
        SET titulo=%s,
            descripcion=%s 
        WHERE id = %s""",(titulo,descripcion,id))
        mysql.connection.commit()
        flash(f"Publicacion: {titulo} actualizada.")
    
    return redirect(url_for("index"))


@app.route('/edit/<int:id>/', methods=['GET', 'POST'])
def edit_publicacion(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * from publicaciones where id = {id};")
        publicacion =cur.fetchall()[0]
    except (MySQL.Error, MySQL.Warning) as e:
        flash(e)
    finally:
        cur.close()

    return render_template('edit-publicacion.html',publicacion=publicacion)

def getPublicacionById(id):

@app.route('/usuarios/')
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




if __name__ == '__main__':
    csrf.init_app(app)
    app.run(port = 3000)
