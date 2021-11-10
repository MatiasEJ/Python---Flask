from flask.helpers import url_for
from flask.templating import render_template
from flask import request,session,flash
from werkzeug.utils import redirect
from forms import PublicacionForm
from app import app,mysql
import consultasPublicacion
from servicesSession import set_session_username 

#CREA PUBLICACIONES
@app.route('/publicacion/', methods=['GET', 'POST'])
def altaPublicacion():
    title = "Alta Publicacion"
    desc_form = PublicacionForm(request.form)
    titulo = desc_form.titulo.data
    descripcion = desc_form.descripcion.data

    if request.method == 'POST' and desc_form.validate() and 'username' in session:
        username = session['username']
        # usuario = consultasPublicacion.get_usuario_by_username(username)
        if (consultasPublicacion.crearPublicacion(titulo,descripcion,username)):
            flash(f"Publicacion:{desc_form.titulo.data}, creada con exito.")
            return redirect(url_for("publicaciones"))
        else:
            flash(f"Error al crear publicacion. Intentelo de nuevo")
            return redirect(url_for("altaPublicacion"))


    return render_template('create_publicacion.html', title=title, form=desc_form, username = set_session_username() )

#LISTA DE TODAS LAS PUBLICACIONES
@app.route('/publicaciones', methods=['GET'])
def publicaciones():
    error = ""
    msgError = ""
    data = consultasPublicacion.get_all_publicaciones()

    if len(data) == 0:
        error = "Lista Vacia"
        msgError = "No existen publicaciones del usuario."

    return render_template('publicaciones.html', error=error, msgError=msgError, publicaciones=data,username = set_session_username())

@app.route('/publicacion/<int:id>/',methods=['GET'])
def get_publicacion(id):
    publicacion = consultasPublicacion.get_publicacion_by_id(id)

    return render_template('publicacion.html', publicacion = publicacion,username = set_session_username() )

@app.route('/delete/<int:id>/', methods=['GET', 'POST'])
def delete_publicacion(id):
    consultasPublicacion.delete_publicacion_by_id(id)
    return redirect(url_for("publicaciones"))


# La pagina donde se edita 
@app.route('/edit/<int:id>/', methods=['GET', 'POST'])
def edit_publicacion(id):
    publicacion = consultasPublicacion.get_publicacion_by_id(id)
    if publicacion == "error":
            return redirect(url_for("publicaciones"))

    return render_template('edit-publicacion.html',publicacion=publicacion)

# Aca se realiza el update
@app.route('/update/<int:id>/',methods=['GET','POST'])
def update_publicacion(id):
    desc_form = PublicacionForm(request.form)
    titulo = desc_form.titulo.data
    descripcion = desc_form.descripcion.data

    if request.method == 'POST' and desc_form.validate():
        consultasPublicacion.update_publicacion(titulo,descripcion,id)

    return redirect(url_for("publicaciones"))



