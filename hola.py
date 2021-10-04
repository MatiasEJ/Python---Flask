from flask import Flask
from flask import request
from flask.templating import render_template
import form
from flask import request

app = Flask(__name__)
app.config['DEV'] = True

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/publicacion/',methods =['GET','POST'])
def altaPublicacion():
    title = "Alta Publicacion"
    desc_form = form.PublicacionForm(request.form)

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

if __name__ == '__main__':
    app.run(port = 3000,debug = True)

