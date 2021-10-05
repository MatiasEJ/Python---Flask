from wtforms import Form 
from wtforms import StringField, TextField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms import HiddenField

class LoginForm(Form):
    username = StringField('Username',[
        validators.length(min=5,max=25,message="Ingrese Titulo valido"),
        validators.Required(message="Username es requerido")
        ]) 
    password = TextField('Password',[
        validators.length(max=255,message="El tamaño maximo es 255"),
        validators.Required(message="Password Requerido")
    ])

    # def validate_username(form,field):
    #     username= field.data
    #     cur = mysql.connection.cursor()
    #     cur.execute("SELECT username FROM usuarios where username = %s",(username))
    #     usuario = cur.fetchall()[0]
    #     if usuario (not None):
    #         raise validators.ValidationError("el usuario ya existe")
            

class PublicacionForm(Form):
    titulo = StringField('Titulo',[
        validators.length(min=4,max=25,message="Ingrese Titulo valido"),
        validators.Required(message="titulo es requerido")
        ]) 
    descripcion = TextField('Descripcion',[
        validators.length(max=255,message="El tamaño maximo es 255")
    ])


