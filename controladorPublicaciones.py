from logging import error
from flask.helpers import url_for
from flask.templating import render_template
from flask import request,session,flash
from werkzeug.utils import redirect
from forms import PublicacionForm
from app import app,mysql
import publicacionServices
from servicesSession import set_session_username 

#CREA PUBLICACIONES
@app.route('/publicacion/', methods=['GET', 'POST'])
def altaPublicacion():
    title = "Alta Publicacion"
    desc_form = PublicacionForm(request.form)

    if request.method == 'POST' and desc_form.validate() and 'username' in session:
        if (publicacionServices.crearPublicacion(desc_form) == True):
            app.logger.warn("SE CREO LA PUBLI")
            flash("publicacion creada")
            return redirect(url_for("publicaciones"))

    return render_template('create_publicacion.html', title=title, form=desc_form, username = set_session_username() )

#LISTA DE TODAS LAS PUBLICACIONES
@app.route('/publicaciones', methods=['GET'])
def publicaciones():
    error = ""
    msgError = ""
    data = publicacionServices.get_all_publicaciones()

    if len(data) == 0:
        error = "Lista Vacia"
        msgError = "No existen publicaciones del usuario."

    return render_template('publicaciones.html', error=error, msgError=msgError, publicaciones=data,username = set_session_username())

@app.route('/publicacion/<int:id>/',methods=['GET'])
def get_publicacion(id):
    publicacion = publicacionServices.get_publicacion_by_id(id)

    return render_template('publicacion.html', publicacion = publicacion,username = set_session_username() )

@app.route('/delete/<int:id>/', methods=['GET', 'POST'])
def delete_publicacion(id):
    publicacionServices.delete_publicacion_by_id(id)
    return redirect(url_for("publicaciones"))


# La pagina donde se edita 
@app.route('/edit/<int:id>/', methods=['GET', 'POST'])
def edit_publicacion(id):
    publicacion = publicacionServices.get_publicacion_by_id(id)
    if publicacion == "error":
            return redirect(url_for("publicaciones"))

    return render_template('edit-publicacion.html',publicacion=publicacion)

# Aca se realiza el update
@app.route('/update/<int:id>/',methods=['GET','POST'])
def update_publicacion(id):
    desc_form = PublicacionForm(request.form)
    if request.method == 'POST':
        publicacionServices.update_publicacion(desc_form,id)
    return redirect(url_for("publicaciones"))



