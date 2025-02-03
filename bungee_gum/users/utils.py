from bungee_gum import db, bcrypt, mail
from flask import render_template, redirect, flash, url_for, request, current_app
import secrets
import os
from PIL import Image
from flask_mail import Message


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile-pics', picture_fn)

    output_size = (450, 450)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


# i SHOULD make it so the old ones are deleted


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(subject="Password Reset Request", sender="noreply@demo.com", recipients=[user.email])

    msg.body = f"""To reset your password, visit the following link 
{url_for("users.reset_token", token=token, _external=True)}

If you did not make this request, then simply ignore this email. 
    """
    mail.send(msg)




