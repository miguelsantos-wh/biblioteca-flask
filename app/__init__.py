from flask import Flask
from flask_bootstrap import Bootstrap
# from flask_uploads import UploadSet, configure_uploads, IMAGES
# from flask_login import LoginManager
# from werkzeug.utils import secure_filename

from .config import Config
# from .auth import auth
# from .models import UserModel

# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'


# @login_manager.user_loader
# def load_user(username):
#     return UserModel.query(username)


def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)

    app.config['SECRET_KEY'] = 'SUPER SECRETO'
    app.config['UPLOADED_PHOTOS_DEST'] = 'app/media'
    app.config['UPLOADED_PHOTOS_PATH'] = 'media'
    app.config.from_object(Config)

    # Configuración de la carga de archivos
    # app.config['UPLOADED_PHOTOS_DEST'] = 'uploads/images'  # Carpeta para guardar las imágenes
    # photos = UploadSet('photos', IMAGES)
    # configure_uploads(app, photos)

    # login_manager.init_app(app)

    # app.register_blueprint(auth)

    return app
