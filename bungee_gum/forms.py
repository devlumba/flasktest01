from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, EmailField, IntegerField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError
import email_validator
from bungee_gum.models import User
from flask_login import current_user


class MyForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])







