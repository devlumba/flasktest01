import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from bungee_gum.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message_category = "danger"

mail = Mail()

# i need to restart my pc in order for variables to supposedly work


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from bungee_gum.main.routes import main
    app.register_blueprint(main)
    from bungee_gum.users.routes import users
    app.register_blueprint(users)
    from bungee_gum.posts.routes import posts
    app.register_blueprint(posts)

    return app
