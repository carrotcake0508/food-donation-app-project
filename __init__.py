from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:IL0veW%40termelon@localhost/food_donation'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
