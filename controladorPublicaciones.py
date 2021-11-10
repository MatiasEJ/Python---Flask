from app import app
from forms import PublicacionForm
from flask import session, flash,render_template,request,redirect,url_for
import consultasPublicacion
from servicesSession import set_session_username 
from errorDb import NotFoundError

#CREA PUBLICACIONES
@app.route('/publicacion', methods=['GET', 'POST'])
def altaPublicacion():
    title = "Alta Publicacion"
    desc_form = PublicacionForm(request.form)
    titulo = desc_form.titulo.data
    descripcion = desc_form.descripcion.data

    if request.method == 'POST' and desc_form.validate() and 'username' in session:
        username = session['username']
        # usuario = consultasPublicacion.get_usuario_by_username(username)
        if (consultasPublicacion.crearPublicacion(titulo,descripcion,username)==True):
            flash(f"Publicacion:{desc_form.titulo.data}, creada con exito.")
        else:
            flash(f"Error al crear publicacion. Intentelo de nuevo en unos minutos.")


    return render_template('create_publicacion.html', title=title, form=desc_form, username = set_session_username() )

#LISTA DE TODAS LAS PUBLICACIONES
@app.route('/publicaciones', methods=['GET'])
def publicaciones():
    error = ""
    msgError = ""
    username = set_session_username() 
    data = consultasPublicacion.get_all_publicaciones_by_username(username)
    if len(data) == 0:
        error = "Lista Vacia"
        msgError = "No existen publicaciones del usuario."

    return render_template('publicaciones.html', error=error, msgError=msgError, publicaciones=data,username = username)

@app.route('/publicacion/<int:id>/',methods=['GET'])
def get_publicacion(id):
    publicacion = consultasPublicacion.get_publicacion_by_id(id)
    
    if publicacion == False:
        flash("No existe la publicacion")
        return redirect(url_for("publicaciones"))
        
    return render_template('publicacion.html', publicacion = publicacion,username = set_session_username() )

@app.route('/delete/<int:id>/', methods=['GET', 'POST'])
def delete_publicacion(id):
    publicacion = consultasPublicacion.delete_publicacion_by_id(id)
    app.logger.warn("borrando la publicacion")
    if publicacion == False:
        flash("No se pudo borrar la publicacion")
        return redirect(url_for("index"))

    return redirect(url_for("publicaciones"))


# La pagina donde se edita 
@app.route('/edit/<int:id>/', methods=['GET', 'POST'])
def edit_publicacion(id):
    username = session['username']
    publicacion = consultasPublicacion.get_publicacion_by_id(id)
    if publicacion == "error":
            return redirect(url_for("publicaciones"))

    return render_template('edit-publicacion.html',publicacion=publicacion, username =username)

# Aca se realiza el update
@app.route('/update/<int:id>/',methods=['GET','POST'])
def update_publicacion(id):
    desc_form = PublicacionForm(request.form)
    titulo = desc_form.titulo.data
    descripcion = desc_form.descripcion.data

    if request.method == 'POST' and desc_form.validate():
        consultasPublicacion.update_publicacion(titulo,descripcion,id)

    return redirect(url_for("publicaciones"))



