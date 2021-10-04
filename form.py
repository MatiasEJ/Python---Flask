from wtforms import Form 
from wtforms import StringField, TextField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms import HiddenField

def length_honey(form, field):
    if len(field.data)>0:
        raise validators.ValidationError('El campo debe estar vacio')

class PublicacionForm(Form):
    titulo = StringField('Titulo',[
        validators.length(min=4,max=25,message="Ingrese Titulo valido"),
        validators.Required(message="titulo es requerido")
        ]) 
    descripcion = TextField('Descripcion',[
        validators.length(max=255,message="El tamaño maximo es 255")
    ])
    honeypot = HiddenField('',[length_honey])