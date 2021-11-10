from app import app
from flask import request,flash,render_template,make_response
from forms import UsuarioForm


@app.route('/create_user/',methods=['GET','POST'])
def create_user():
    title = "Alta Usuarios"
    form = UsuarioForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        # CREA USUARIO, FALTA IMPLEMENTAR
        flash(f"Usuario: {username} creado")
    
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





