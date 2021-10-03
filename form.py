from wtforms import Form 
from wtforms import StringField, TextField
from wtforms.fields.html5 import EmailField

class PublicacionForm(Form):
    titulo = StringField('titulo') 
    descripcion = TextField('descripcion') 