from flask import Flask
from flask.helpers import url_for
from flask.templating import render_template
from flask import request
from flask import g
from flask_wtf import CSRFProtect
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
from flask import session
from forms import LoginForm
import os
from werkzeug.utils import secure_filename
 


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

mysql = MySQL(app)
csrf = CSRFProtect(app)

@app.errorhandler(404)
def page_not_found(e):
    title = "404"
    msg = "Page not found."
    return render_template('404.html', title=title, msg=msg), 404


@app.route('/')
def index():
    title = "Home"
    username = ""
    publicaciones = consultasPublicacion.get_all_publicaciones()

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

@app.before_request
def before_request():
    # chequeo de datos de session/DBs
    # GLOBAL malapractica?
    g.username = ""
    if 'username' in session:
        g.username =  session['username']
    
    g.test = 'TEST' 


@app.after_request
def after_request(res):
    # chequeo de datos de session
    return res

 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

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
