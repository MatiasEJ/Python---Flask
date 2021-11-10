from app import app
from flask import session, flash,render_template,request,redirect,url_for
from consultasPublicacion import get_all_publicaciones
from forms import LoginForm

@app.route('/')
def index():
    title = "Home"
    username = ""
    publicaciones = get_all_publicaciones()

    if len(publicaciones) == 0:
        error = "No existen publicaciones"
        app.logger.warn(error)
        flash(error)

    if 'username' in session:
        username = session['username']
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
    if request.method == 'POST' and desc_form.validate() :
        username = desc_form.username.data
        session['username'] = username
        return redirect(url_for("index"))
    return render_template('login.html', form=desc_form)

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for("index"))