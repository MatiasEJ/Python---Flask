from flask import Flask
from flask.templating import render_template
from flask import g
from flask_wtf import CSRFProtect
from flask_mysqldb import MySQL
from flask import session

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config.from_object('config.DevelopmentConfig')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mysql = MySQL(app)
csrf = CSRFProtect(app)

from controladorUsuario import *
from controladorLogin import *
from controladorPublicaciones import *

@app.errorhandler(404)
def page_not_found(e):
    title = "404"
    msg = "Page not found."
    return render_template('404.html', title=title, msg=msg), 404






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

 

# @app.route('/ajax-login',methods=['POST'])
# def ajax_login():
#     username = request.form['username']
#     # Validation
#     res = {'status':200,'username':username, 'id':1}
#     return json.dumps(res)




if __name__ == '__main__':
    csrf.init_app(app)
    app.run(port = 3000)
