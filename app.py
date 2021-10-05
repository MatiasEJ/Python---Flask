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


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
mysql = MySQL(app)

csrf = CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    title="404"
    msg="Page not found."
    return render_template('404.html',title = title,msg = msg),404

@app.before_request
def before_request():
    #chequeo de datos de session/DBs
    g.test = 'TEST' #GLOBAL? malapractica?

@app.after_request
def after_request(res):
    #chequeo de datos de session
    return res

@app.route('/')
def index():
    print("index--->")
    print(g.test)
    custom_cookie = request.cookies.get('custom_cookie','Undefined')
    print(custom_cookie)
    if 'username' in session:
        username = session['username']
        print(username)

    return render_template('index.html') 

@app.route('/login',methods=['GET','POST'])
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



    return render_template('login.html',title = title, form = desc_form) 

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for("login")) 

@app.route('/publicacion',methods =['GET','POST'])
def altaPublicacion():
    TABLA = 'publicaciones'
    title = "Alta Publicacion"
    desc_form = PublicacionForm.PublicacionForm(request.form)
    msg_publi = ""
    if request.method == 'POST' and desc_form.validate():
        titulo = desc_form.titulo.data
        print(titulo)
        descripcion = desc_form.descripcion.data
        print(descripcion)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO publicaciones (titulo, descripcion) VALUES (%s,%s)",(titulo,descripcion))
        mysql.connection.commit()
        msg_publi = "Publicación creada."


    return render_template('altaPublicacion.html',title = title, form = desc_form, msg = msg_publi) 

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
    #Validation
    res = {'status':200,'username':username, 'id':1}
    return json.dumps(res)




if __name__ == '__main__':
    csrf.init_app(app)
    app.run(port = 3000)

