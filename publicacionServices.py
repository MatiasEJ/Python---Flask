
from app import mysql
from flask import flash
from flask import session
from flask_mysqldb import MySQL, MySQLdb
from werkzeug.utils import redirect
from flask.helpers import url_for
from controladorPublicaciones import *

from errorDb import NotFoundError

def crearPublicacion(desc_form)->bool:
    titulo = desc_form.titulo.data
    descripcion = desc_form.descripcion.data
    conexion = False
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO publicaciones (titulo, descripcion) VALUES (%(titulo)s,%(descripcion)s)", {'titulo':titulo,'descripcion':descripcion})
        mysql.connection.commit()
        flash("Publicacion creada. Autor: "+session['username'])
        conexion = True 
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        flash(e)
        conexion =  False
    finally:
        cur.close()
    return conexion

def get_publicacion_by_id(id):
    resultado = None
    try:
        cur = mysql.connection.cursor()
        # TODO : INSEGURO? PORQUE?... 
        cur.execute(f"SELECT * from publicaciones where id = {id};")
        resultado =cur.fetchall()[0]
    except IndexError:
        resultado = "error"
        flash("No se encuentra la publicacion!!!")
    finally:
        cur.close()
    # Aca chequeo si la tupla tiene items 
    return resultado

def get_all_publicaciones()-> list:
    data= [] 
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM publicaciones")
        data = cur.fetchall()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        flash(e)
    finally:
        cur.close()
    return data

def delete_publicacion_by_id(id):
    try:
        cur = mysql.connection.cursor()
        publicacion= get_publicacion_by_id(id)
        if publicacion == None:
            flash("No se encuentra la publicacion")
            raise NotFoundError()

        cur.execute(f"DELETE from publicaciones where id = {id};")
        mysql.connection.commit()
        flash(f"Publicacion: {publicacion} eliminada.")
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        flash(e)
    finally:
        cur.close()

def update_publicacion(desc_form,id):
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
        

