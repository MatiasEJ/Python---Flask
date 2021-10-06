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
from flask_mysqldb import MySQL
from app import app
from app import mysql
from errorDb import NotFoundError,NotAuthError 

@app.route('/publicacion/', methods=['GET', 'POST'])
def altaPublicacion():
    title = "Alta Publicacion"
    desc_form = PublicacionForm(request.form)
    
    if request.method == 'POST' and desc_form.validate():
        titulo = desc_form.titulo.data
        descripcion = desc_form.descripcion.data
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO publicaciones (titulo, descripcion) VALUES (%s,%s)", (titulo, descripcion))
            mysql.connection.commit()
            flash("Publicacion creada.")
        except (MySQL.Error, MySQL.Warning) as e:
            app.logger.warn("wat")
            flash(e)
        finally:
            cur.close()
    return render_template('altaPublicacion.html', title=title, form=desc_form )


@app.route('/publicaciones', methods=['GET'])
def publicaciones():
    error = ""
    msgError = ""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM publicaciones")
        data = cur.fetchall()
    except:
        error = "Error conexion db"
        msgError = "No se pudo conectar a la base de datos."

    if len(data) == 0:
        error = "Lista Vacia"
        msgError = "No existen publicaciones del usuario."

    return render_template('publicaciones.html', error=error, msgError=msgError, publicaciones=data)


@app.route('/delete/<int:id>/', methods=['GET', 'POST'])
def delete_publicacion(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * from publicaciones where id = {id};")
        publicacion =cur.fetchall()[0]

        if publicacion == None:
            msg = "No se encuentra la publicacion"
            flash(msg)
            raise NotFoundError(msg)

        cur.execute(f"DELETE from publicaciones where id = {id};")
        mysql.connection.commit()
        flash(f"Publicacion: {publicacion} eliminada.")
    except (MySQL.Error, MySQL.Warning) as e:
        flash(e)
    finally:
        cur.close()
    return redirect(url_for("publicaciones"))

@app.route('/update/<int:id>/',methods=['GET','POST'])
def update_publicacion(id):
    desc_form = PublicacionForm(request.form)
    if request.method == 'POST':
        try:
            cur = mysql.connection.cursor()
            titulo = desc_form.titulo.data 
            descripcion = desc_form.descripcion.data 
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




