from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField,SelectField

class AddForm(FlaskForm):
    titulo = StringField('Titulo Nuevo Blog')
    selec = SelectField(u'¿El blog sera privado o publico?',choices=[('Opcion1','Privado'),('opcion2','publico')])
    submit = SubmitField('Añadir nuevo blog')

class DelForm(FlaskForm):
    id = IntegerField('Id Number of puppy to remove: ')
    submit = SubmitField("remove puppy")