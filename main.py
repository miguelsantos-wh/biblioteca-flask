import unittest
import os

from flask import Flask
from app import create_app
from datetime import datetime
from google.cloud import firestore
from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash

from app.firestore_service import (get_editores, put_editor, get_editor, update_editor, delete_editor, get_autores,
                                   put_autor, get_autor, update_autor, delete_autor, update_libro, put_libro,
                                   get_libros)
from app.forms import AgregarEditorForm, AgregarAutorForm, AgregarLibroForm
from werkzeug.utils import secure_filename

app = create_app()


# @app.route('/')
# def hello():
#     return 'Hello Flask!'


@app.route('/')
def index_biblioteca():
    return render_template('index.html')


@app.route('/editores/lista/')
def lista_editores():
    editores = get_editores()
    return render_template('editor_list.html', editores=editores)


@app.route('/editores/agregar/', methods=['GET', 'POST'])
def agregar_editor():
    editor_form = AgregarEditorForm()

    if editor_form.validate_on_submit():
        nuevo_editor = {
            'nombre': editor_form.nombre.data,
            'domicilio': editor_form.domicilio.data,
            'ciudad': editor_form.ciudad.data,
            'estado': editor_form.estado.data,
            'pais': editor_form.pais.data,
            'website': editor_form.website.data,
        }
        put_editor(nuevo_editor)
        flash('Editor agregado con éxito!')
        return redirect(url_for('lista_editores'))

    return render_template('editor_form.html', editor_form=editor_form)


@app.route('/editores/<editor_id>/')
def obtener_editor(editor_id):
    editor_data = get_editor(editor_id)

    if editor_data.exists:
        editor = editor_data.to_dict()
    else:
        flash('El editor no existe!', 'error')
        return redirect(url_for('lista_editores'))
    return render_template('editor_detail.html', editor=editor, editor_id=editor_id)


@app.route('/editores/modificar/<editor_id>/', methods=['GET', 'POST'])
def editar_editor(editor_id):
    editor_data = get_editor(editor_id)
    editor_form = AgregarEditorForm()
    if request.method == 'GET':
        if editor_data.exists:
            editor = editor_data.to_dict()
            editor_form = AgregarEditorForm(data=editor)
        else:
            flash('El editor no existe!', 'error')
            return redirect(url_for('lista_editores'))
    else:
        if editor_form.validate_on_submit():
            update_editor(editor_form, editor_id)
            flash('Editor modificado con éxito!')
            return redirect(url_for('lista_editores'))
    return render_template('editor_form.html', editor_data=editor, editor_form=editor_form)


@app.route('/editores/elimiar/<editor_id>/', methods=['GET', 'POST'])
def eliminar_editor(editor_id):
    editor_data = get_editor(editor_id)
    if request.method == 'GET':
        if editor_data.exists:
            editor = editor_data.to_dict()
        else:
            flash('El editor no existe!', 'error')
            return redirect(url_for('lista_editores'))
    else:
        delete_editor(editor_id)
        flash('Editor eliminado con éxito!')
        return redirect(url_for('lista_editores'))
    return render_template('editor_delete.html', editor_data=editor)


@app.route('/autores/lista/')
def lista_autores():
    autores = get_autores()
    return render_template('autor_list.html', autores=autores)


@app.route('/autores/agregar/', methods=['GET', 'POST'])
def agregar_autor():
    autor_form = AgregarAutorForm()

    if autor_form.validate_on_submit():
        put_autor(autor_form)
        flash('Autor agregado con éxito!')
        return redirect(url_for('lista_autores'))

    return render_template('autor_form.html', autor_form=autor_form)


@app.route('/autores/<autor_id>/')
def obtener_autor(autor_id):
    autor_data = get_autor(autor_id)

    if autor_data.exists:
        autor = autor_data.to_dict()
    else:
        flash('El autor no existe!', 'error')
        return redirect(url_for('lista_autores'))
    return render_template('autor_detail.html', autor=autor, autor_id=autor_id)


@app.route('/autores/modificar/<autor_id>/', methods=['GET', 'POST'])
def editar_autor(autor_id):
    autor_data = get_autor(autor_id)
    autor_form = AgregarAutorForm()
    if request.method == 'GET':
        if autor_data.exists:
            autor = autor_data.to_dict()
            autor_form = AgregarAutorForm(data=autor)
        else:
            flash('El autor no existe!', 'error')
            return redirect(url_for('lista_autores'))
    else:
        if autor_form.validate_on_submit():
            update_autor(autor_form, autor_id)
            flash('Autor modificado con éxito!')
            return redirect(url_for('lista_autores'))
    return render_template('autor_form.html', autor_data=autor, autor_form=autor_form)


@app.route('/autores/elimiar/<autor_id>/', methods=['GET', 'POST'])
def eliminar_autor(autor_id):
    autor_data = get_autor(autor_id)
    if request.method == 'GET':
        if autor_data.exists:
            autor = autor_data.to_dict()
        else:
            flash('El autor no existe!', 'error')
            return redirect(url_for('lista_editores'))
    else:
        delete_autor(autor_id)
        flash('Autor eliminado con éxito!')
        return redirect(url_for('lista_autores'))
    return render_template('autor_delete.html', autor_data=autor)


@app.route('/libros/lista/')
def lista_libros():
    libros = get_libros()
    autores = get_autores()
    autores_data = {}
    for autor in autores:
        autores_data[autor.id] = autor.to_dict()
    # for libro in libros:
    #     libro = libro.to_dict()
    #     autores_id = libro.get('autores_id')
    #     autores = []
    #     if autores_id:
    #         for autor in autores_id:
    #             autores.append(get_autor(autor))
    #     libro.update({'autores': autores})
    #     libros_data.append(libro)

    return render_template('libro_list.html', libros=libros, autores=autores_data)


@app.route('/libros/agregar/', methods=['GET', 'POST'])
def agregar_libro():
    libro_form = AgregarLibroForm()
    editores = get_editores()
    autores = get_autores()

    # Llenar opciones del campo "Editor"
    libro_form.editor_id.choices = [(editor.id, editor.to_dict()['nombre']) for editor in editores]

    # Llenar opciones del campo "Autores"
    libro_form.autores_id.choices = [(autor.id, autor.to_dict()['nombre']) for autor in autores]

    if libro_form.validate_on_submit():
        portada = libro_form.portada.data  # Obtener la imagen subida
        filename = secure_filename(portada.filename)
        portada_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)
        portada.save(portada_path)
        fecha_publicacion_str = libro_form.fecha_publicacion.data.strftime('%Y-%m-%d')
        fecha_publicacion = datetime.strptime(fecha_publicacion_str, '%Y-%m-%d')
        fecha_timestamp = firestore.SERVER_TIMESTAMP if fecha_publicacion is None else fecha_publicacion
        put_libro(libro_form, portada_path, fecha_timestamp)
        flash('Libro agregado con éxito!')
        return redirect(url_for('lista_autores'))

    return render_template('libro_form.html', libro_form=libro_form)
