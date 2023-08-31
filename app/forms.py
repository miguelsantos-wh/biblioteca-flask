from flask_wtf import FlaskForm
from wtforms.fields import (StringField, PasswordField, SubmitField, EmailField, FileField, SelectField,
                            SelectMultipleField, DateField)
from wtforms.validators import DataRequired
from wtforms import widgets


class AgregarEditorForm(FlaskForm):
    nombre = StringField('Nombre completo: ', render_kw={"class": "form-control"}, validators=[DataRequired()])
    domicilio = StringField('Domicilio: ', render_kw={"class": "form-control"}, validators=[DataRequired()])
    ciudad = StringField('Ciudad: ', render_kw={"class": "form-control"}, validators=[DataRequired()])
    estado = StringField('Estado: ', render_kw={"class": "form-control"}, validators=[DataRequired()])
    pais = StringField('Pais: ', render_kw={"class": "form-control"}, validators=[DataRequired()])
    website = StringField('Pagina Web: ', render_kw={"class": "form-control"}, validators=[DataRequired()])


class AgregarAutorForm(FlaskForm):
    nombre = StringField('Nombre: ', render_kw={"class": "form-control"}, validators=[DataRequired()])
    apellidos = StringField('Apellidos: ', render_kw={"class": "form-control"}, validators=[DataRequired()])
    email = EmailField('Correo electrónico: ', render_kw={"class": "form-control"}, validators=[DataRequired()])


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AgregarLibroForm(FlaskForm):
    titulo = StringField('Titulo del libro: ', render_kw={"class": "form-control"}, validators=[DataRequired()])
    autores_id = MultiCheckboxField('Autores: ', coerce=str)
    editor_id = SelectField('Editor: ', coerce=str, render_kw={"class": "form-control"}, validators=[DataRequired()])
    fecha_publicacion = DateField('Fecha de publicación: ', format='%Y-%m-%d', render_kw={"class": "form-control"}, validators=[DataRequired()])
    portada = FileField('Portada: ', render_kw={"class": "form-control"})
