from wtforms import Form, StringField, TextField,validators,HiddenField
from wtforms.fields.core import BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.fields.simple import SubmitField
from flask_wtf import FlaskForm

class UsuarioForm(Form):
    nombre = StringField('Nombre',[
        validators.length(min=5,max=25,message="Ingrese Titulo valido"),
        validators.Required(message="Username es requerido")
        ]) 
    apellido = StringField('Apellido',[
        validators.length(min=5,max=25,message="Ingrese Titulo valido"),
        validators.Required(message="Username es requerido")
        ]) 
    direccion = StringField('Direccion',[
        validators.length(min=5,max=25,message="Ingrese Titulo valido"),
        validators.Required(message="Username es requerido")
        ]) 
    username = StringField('Username',[
        validators.length(min=5,max=25,message="Ingrese Titulo valido"),
        validators.Required(message="Username es requerido")
        ]) 
    password = TextField('Password',[
        validators.length(max=255,message="El tamaño maximo es 255"),
        validators.Required(message="Password Requerido")
    ])

    # CUSTOM VALIDATIONS
    # def validate_username(form,field):
    #     username= field.data
    #     cur = mysql.connection.cursor()
    #     cur.execute("SELECT username FROM usuarios where username = %s",(username))
    #     usuario = cur.fetchall()[0]
    #     if usuario (not None):
    #         raise validators.ValidationError("el usuario ya existe")
            

class PublicacionForm(Form):
    titulo = StringField('titulo',[
        validators.length(min=4,max=25,message="Ingrese Titulo valido. Entre 4 y 25 caracteres."),
        validators.Required(message="titulo es requerido")
        ]) 
    descripcion = TextField('descripcion',[
        validators.length(max=255,message="El tamaño maximo es 255")
    ])



class LoginForm(FlaskForm):
    username = StringField('username',[
        validators.length(min=5,max=25,message="Ingrese usuario valido. Entre 5 y 25 caracteres."),
        validators.Required(message="Username es requerido")
        ]) 
    password = StringField('password',[
        validators.length(min=5,max=25,message="Ingrese password valido"),
        validators.Required(message="Username es requerido")
        ]) 
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')