import firebase_admin
from firebase_admin import credentials, firestore

credential = credentials.ApplicationDefault()
firebase_admin.initialize_app()

db = firestore.client()


def get_libros():
    return db.collection('libros').get()


def get_libro(libro_id):
    return db.collection('libros').document(libro_id).get()


def get_editores():
    return db.collection('editores').get()


def get_editor(editor_id):
    return db.collection('editores').document(editor_id).get()


def get_autores():
    return db.collection('autores').get()


def get_autor(autor_id):
    return db.collection('autores').document(autor_id).get()


def put_libro(libro_data, portada_path,fecha_publicacion):
    libro_put = {
        'titulo': libro_data.titulo.data,
        'fecha_publicacion': fecha_publicacion,
        'portada': portada_path,
        'editor_id': libro_data.editor_id.data,
        'autores_id': libro_data.autores_id.data,
    }
    db.collection('libros').add(libro_put)


def put_editor(editor_data):
    editor_put = {
        'nombre': editor_data.get("nombre"),
        'domicilio': editor_data.get("domicilio"),
        'ciudad': editor_data.get("ciudad"),
        'estado': editor_data.get("estado"),
        'pais': editor_data.get("pais"),
        'website': editor_data.get("website"),
    }
    db.collection('editores').add(editor_put)


def put_autor(autor_data):
    autor_put = {
        'nombre': autor_data.nombre.data,
        'apellidos': autor_data.apellidos.data,
        'email': autor_data.email.data,
    }
    db.collection('autores').add(autor_put)


def update_libro(libro_data, portada_path):
    libro_ref = db.collection('libros').document(libro_data_id)
    libro_ref.update({
        'titulo': libro_data.titulo.data,
        'fecha_publicacion': libro_data.fecha_publicacion.data,
        'portada': portada_path,
        'editor_id': libro_data.editor_id.data,
        'autores_id': libro_data.autores_id.data,
    })


def update_editor(editor_data, editor_id):
    editor_ref = db.collection('editores').document(editor_id)
    editor_ref.update({
        'nombre': editor_data.nombre.data,
        'domicilio': editor_data.domicilio.data,
        'ciudad': editor_data.ciudad.data,
        'estado': editor_data.estado.data,
        'pais': editor_data.pais.data,
        'website': editor_data.website.data,
    })


def update_autor(autor_data, autor_id):
    autor_ref = db.collection('autores').document(autor_id)
    autor_ref.update({
        'nombre': autor_data.nombre.data,
        'apellidos': autor_data.apellidos.data,
        'email': autor_data.email.data,
    })


def delete_libro(libro_id):
    libro_ref = db.collection('libros').document(libro_id)
    libro_ref.delete()


def delete_editor(editor_id):
    editor_ref = db.collection('editores').document(editor_id)
    editor_ref.delete()


def delete_autor(autor_id):
    autor_ref = db.collection('autores').document(autor_id)
    autor_ref.delete()
