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