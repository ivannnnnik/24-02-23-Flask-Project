from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os

app = Flask(__name__)  # Создаем приложение
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')

app.debug = True

# БД
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Авторизация
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
app.app_context().push()

from . import views
