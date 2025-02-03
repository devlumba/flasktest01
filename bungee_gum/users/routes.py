from flask import Blueprint
from bungee_gum import app, db, bcrypt, mail
from bungee_gum.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm,
                                    ResetPasswordForm)
from flask import render_template, redirect, flash, url_for, request
from bungee_gum.models import Post, User
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import desc, asc, select

from bungee_gum.users.utils import save_picture, send_reset_email

users = Blueprint("users", __name__)


@users.route("/register/", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You already are authenticated. Please log out in order to get to that page.", "info")
        return redirect(url_for("main.home"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"whubbalubbadubdub account created for {form.email.data}, you can go and login wubbadubba", "info")
        return redirect(url_for('users.login'))

    return render_template("register.html", title="Register", form=form)


@users.route("/login/", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        flash("You already are authenticated. Please log out in order to get to that page.", "info")
        return redirect(url_for("main.home"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f"i was the knight in shining armor in your movie(login successful)", "info")
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        # i could use else down here, but it doesn't seem to have meaning to
        flash(f"whubbalubbadubdub nope {form.email.data}, check yo email and password", "danger")

    return render_template("login.html", title="Login", form=form)


@users.route("/logout/")
def logout():
    if current_user.is_authenticated:
        flash("You've been logged out successfully", "info")
        logout_user()
        return redirect(url_for("main.home"))
    flash("You aren't logged in yet", "danger")
    return redirect(url_for("main.home"))


# DEVELOPMENT ONLY
@users.route("/login-admin/")
def login_admin():
    user = User.query.filter_by(email="admin@admin.com").first()
    login_user(user, remember=True)
    flash(f"ADMIN LOGIN SUCCESSFUL", "info")
    return redirect(url_for("main.home"))


@users.route("/user/<int:id>")
def specific_user(id):
    user = User.query.get_or_404(id)
    posts = Post.query.order_by(desc("date_posted")).filter_by(user_id=user.id).all()
    posts_num = Post.query.filter_by(user_id=user.id).count()
    return render_template("specific-user.html", title=f"{user.username}'s Page", user=user,
                           posts=posts, posts_num=posts_num)


@users.route("/login-user/<int:id>")
def login_specific_user(id):
    user = User.query.get_or_404(id)
    login_user(user, remember=True)
    flash(f"{user.username} login successful", category="info")
    return redirect(url_for("users.specific_user", id=user.id))


@users.route("/my-account/", methods=["POST", "GET"])
@login_required
def my_account():
    update_form = UpdateAccountForm()
    if update_form.validate_on_submit():
        if update_form.picture.data:
            picture_file = save_picture(update_form.picture.data)
            current_user.image_file = picture_file
        current_user.username = update_form.username.data
        current_user.email = update_form.email.data
        db.session.commit()
        flash("Yo data been updated :3", "info")
        return redirect(url_for('users.my_account'))
    elif request.method == "GET":
        update_form.username.data = current_user.username
        update_form.email.data = current_user.email

    return render_template("my-account.html", title="My Account", update_form=update_form)
    # update_form to avoid forms confusion later on


# login_required with login_view in init seems like useless crap when i can make if current_user.is_aunthenticated
# with nice colourful flash message

@users.route("/all-users/")
def all_users():
    all_users = User.query.all()
    return render_template("all-users.html", title="All Users", all_users=all_users)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        flash("You already are authenticated. Please log out in order to get to that page.", "info")
        return redirect(url_for("main.home"))

    request_form = RequestResetForm()

    if request_form.validate_on_submit():
        user = User.query.filter_by(email=request_form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset the password.", "info")
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", title="Reset Password", request_form=request_form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        flash("You already are authenticated. Please log out in order to get to that page.", "info")
        return redirect(url_for("main.home"))

    user = User.verify_reset_token(token)

    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))

    reset_form = ResetPasswordForm()

    if reset_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(reset_form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash(f"Your password has been updated", "info")
        return redirect(url_for('users.login'))

    return render_template("reset_token.html", title="Reset Password", reset_form=reset_form)

