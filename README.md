# Ingeniería de Software II - 2023

Aplicación web desarrollada en backend con Python (framework Django) para la asignatura Ingeniería de Software II de la Facultad de Informática, UNLP.

## Ejecución local

Instalaciones necesarias:
  - Python 3.10.x
  - virtualenv
  - Django
  - SQLite

Para ejecutar la aplicación es necesario activar el entorno virtual e instalar las dependencias con `pip install -r requirements.txt`. Para migrar la base de datos `python manage.py makemigrations OMDApp` y `python manage.py migrate`. Luego, ejecutar `python manage.py runserver`.
