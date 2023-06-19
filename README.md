# biblioteca-flask

# Instalacion

### 1. Clonar el repositorio
git clone

### 2. Crear entorno dentro la carpeta del proyecto
virtualenv venv --python=python3.8

### 3. El entorno ya se inicializa si se abre en Pycharm, si es por comando es 
source venv/bin/activate

### 4. Instalar requerimientos
pip install -r requirements.txt

### 5. Agregar worker de tipo Flask Server
Target: main.py
FLASK_ENV: development
FLASK_DEBUG: check

Environment variable:
GOOGLE_CLOUD_PROJECT=platzii-flask
