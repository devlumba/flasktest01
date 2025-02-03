from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, IntegerField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=4, max=35)])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")


class SearchForm(FlaskForm):
    bar = StringField("searchbar", validators=[Length(min=0, max=40)])
    submit = SubmitField("Submit")
