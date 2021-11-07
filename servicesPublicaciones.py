
from app import mysql
from flask import flash
from flask import session
from flask_mysqldb import MySQLdb
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
        cur.execute("INSERT INTO publicaciones (titulo, descripcion) VALUES (%s,%s)", (titulo, descripcion))
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
    try:
        cur = mysql.connection.cursor()
        """ TODO : INSEGURO? PORQUE?... """
        cur.execute(f"SELECT * from publicaciones where id = {id};")
        publicacion =cur.fetchall()[0]
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        flash(e)
    finally:
        cur.close()
    return publicacion

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

