from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Конфигурация для подключения к базе данных (например, PostgreSQL)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/phone_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb://your_username:your_password@localhost/phone_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# Инициализация базы данных
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views, models  # Импортируем маршруты и модели
