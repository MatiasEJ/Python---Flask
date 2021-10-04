from flask import Flask
from flask import request
from flask.helpers import url_for
from flask.templating import render_template
from flask import request
from flask import make_response
from flask import session 
from flask import flash
from flask_wtf import CSRFProtect
from werkzeug.utils import redirect
import LoginForm
import PublicacionForm
import json

app = Flask(__name__)
app.config['DEV'] = True
app.secret_key='secret' #Usar variables de sesion
csrf = CSRFProtect(app)

@app.errorhandler(404)
def page_not_found(e):
    title="404"
    msg="Page not found."
    return render_template('404.html',title = title,msg = msg),404

@app.route('/')
def index():
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

@app.route('/publicacion/',methods =['GET','POST'])
def altaPublicacion():
    title = "Alta Publicacion"
    desc_form = PublicacionForm.PublicacionForm(request.form)

    if request.method == 'POST' and desc_form.validate():
        print(desc_form.titulo.data)
        print(desc_form.descripcion.data)

    return render_template('altaPublicacion.html',title = title, form = desc_form) 

@app.route('/usuarios/')
@app.route('/usuarios/<name>/')
@app.route('/usuarios/<name>/<int:id>/')
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
    app.run(port = 3000,debug = True)

