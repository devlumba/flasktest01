import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from bungee_gum.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "danger"

mail = Mail(app)

# i need to restart my pc in order for variables to supposedly work

from bungee_gum.main.routes import main
app.register_blueprint(main)
from bungee_gum.users.routes import users
app.register_blueprint(users)
from bungee_gum.posts.routes import posts
app.register_blueprint(posts)


def create_app(config_class=Config):
    pass


