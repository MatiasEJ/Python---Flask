from logging import raiseExceptions
from flask import Flask, config
from flask import request
from flask.helpers import url_for
from flask.templating import render_template
from flask import request
from flask import make_response
from flask import session
from flask import flash
from flask import g
from werkzeug.utils import redirect
from forms import PublicacionForm
import json
from flask_mysqldb import MySQL,MySQLdb
from app import app
from app import mysql
from errorDb import NotFoundError,NotAuthError
from servicesPublicaciones import crearPublicacion, delete_publicacion_by_id, get_all_publicaciones 

#CREA PUBLICACIONES
@app.route('/publicacion/', methods=['GET', 'POST'])
def altaPublicacion():
    title = "Alta Publicacion"
    desc_form = PublicacionForm(request.form)

    if request.method == 'POST' and desc_form.validate() and 'username' in session:
        if (crearPublicacion(desc_form) == True):
            app.logger.warn("SE CREO LA PUBLI")
            return redirect(url_for("publicaciones"))

    return render_template('create_publicacion.html', title=title, form=desc_form )

#LISTA DE TODAS LAS PUBLICACIONES
@app.route('/publicaciones', methods=['GET'])
def publicaciones():
    error = ""
    msgError = ""
    data = get_all_publicaciones()

    if len(data) == 0:
        error = "Lista Vacia"
        msgError = "No existen publicaciones del usuario."

    return render_template('publicaciones.html', error=error, msgError=msgError, publicaciones=data)


@app.route('/delete/<int:id>/', methods=['GET', 'POST'])
def delete_publicacion(id):
    delete_publicacion_by_id(id)
    return redirect(url_for("publicaciones"))

@app.route('/update/<int:id>/',methods=['GET','POST'])
def update_publicacion(id):
    desc_form = PublicacionForm(request.form)
    if request.method == 'POST':
        try:
            cur = mysql.connection.cursor()
            titulo = desc_form.titulo.data 
            descripcion = desc_form.descripcion.data 
            #ESTA ES LA FORMA DE AGREGAR DATOS.
            cur.execute("""
            UPDATE publicaciones 
            SET titulo=%s,
                descripcion=%s 
            WHERE id = %s""",(titulo,descripcion,id))
            mysql.connection.commit()
            flash(f"Publicacion: {titulo} actualizada.")
        except (MySQL.Error, MySQL.Warning) as e:
            flash(e)
        finally:
            cur.close()
        
    
    return redirect(url_for("publicaciones"))


@app.route('/edit/<int:id>/', methods=['GET', 'POST'])
def edit_publicacion(id):
    publicacion = None
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * from publicaciones where id = {id}")
    try:
        publicacion = cur.fetchall()[0]
    except IndexError:
        flash("No se encuentra la publicacion")

    return render_template('edit-publicacion.html',publicacion=publicacion)




