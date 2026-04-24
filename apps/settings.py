import os

basedir = os.path.dirname(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'app.sqlite')

SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(10)

from pathlib import Path

UPLOAD_FOLDER = str(Path(basedir,'apps','images'))