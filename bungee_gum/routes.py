from bungee_gum import app, db, bcrypt, mail
from bungee_gum.forms import (RegistrationForm, LoginForm, UpdateAccountForm, PostForm, SearchForm, RequestResetForm,
                              ResetPasswordForm)
from flask import render_template, redirect, flash, url_for, request
from bungee_gum.models import Post, User
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image
from sqlalchemy import desc, asc, select
from flask_mail import Message


@app.route("/")
def home():
    return render_template("home.html", title="dInAmIcc tiTle")


@app.route("/test1/")
def test1():
    form = RegistrationForm()
    return render_template("test1.html", title="test1", form=form)


@app.route("/register/", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You already are authenticated. Please log out in order to get to that page.", "info")
        return redirect(url_for("home"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"whubbalubbadubdub account created for {form.email.data}, you can go and login wubbadubba", "info")
        return redirect(url_for('login'))

    return render_template("register.html", title="Register", form=form)


@app.route("/login/", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        flash("You already are authenticated. Please log out in order to get to that page.", "info")
        return redirect(url_for("home"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f"i was the knight in shining armor in your movie(login successful)", "info")
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("home"))
        # i could use else down here, but it doesn't seem to have meaning to
        flash(f"whubbalubbadubdub nope {form.email.data}, check yo email and password", "danger")

    return render_template("login.html", title="Login", form=form)


@app.route("/logout/")
def logout():
    if current_user.is_authenticated:
        flash("You've been logged out successfully", "info")
        logout_user()
        return redirect(url_for("home"))
    flash("You aren't logged in yet", "danger")
    return redirect(url_for("home"))


# DEVELOPMENT ONLY
@app.route("/login-admin/")
def login_admin():
    user = User.query.filter_by(email="admin@admin.com").first()
    login_user(user, remember=True)
    flash(f"ADMIN LOGIN SUCCESSFUL", "info")
    return redirect(url_for("home"))


@app.route("/login-user/<int:id>")
def login_specific_user(id):
    user = User.query.get_or_404(id)
    login_user(user, remember=True)
    flash(f"{user.username} login successful", category="info")
    return redirect(url_for("specific_user", id=user.id))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile-pics', picture_fn)

    output_size = (450, 450)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


# i could make it so the old ones are deleted


@app.route("/my-account/", methods=["POST", "GET"])
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
        return redirect(url_for('my_account'))
    elif request.method == "GET":
        update_form.username.data = current_user.username
        update_form.email.data = current_user.email

    return render_template("my-account.html", title="My Account", update_form=update_form)
    # update_form to avoid forms confusion later on


# login_required with login_view in init seems like useless crap when i can make if current_user.is_aunthenticated
# with nice colourful flash message


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(subject="Password Reset Request", sender="noreply@demo.com", recipients=[user.email])

    msg.body = f"""To reset your password, visit the following link 
{url_for("reset_token", token=token, _external=True)}
    
If you did not make this request, then simply ignore this email. 
    """
    mail.send(msg)


@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        flash("You already are authenticated. Please log out in order to get to that page.", "info")
        return redirect(url_for("home"))

    request_form = RequestResetForm()

    if request_form.validate_on_submit():
        user = User.query.filter_by(email=request_form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset the password.", "info")
        return redirect(url_for("login"))
    return render_template("reset_request.html", title="Reset Password", request_form=request_form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        flash("You already are authenticated. Please log out in order to get to that page.", "info")
        return redirect(url_for("home"))

    user = User.verify_reset_token(token)

    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("reset_request"))

    reset_form = ResetPasswordForm()

    if reset_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(reset_form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash(f"Your password has been updated", "info")
        return redirect(url_for('login'))

    return render_template("reset_token.html", title="Reset Password", reset_form=reset_form)


@app.route("/all-users/")
def all_users():
    all_users = User.query.all()
    return render_template("all-users.html", title="All Users", all_users=all_users)


@app.route("/user/<int:id>")
def specific_user(id):
    user = User.query.get_or_404(id)
    posts = Post.query.order_by(desc("date_posted")).filter_by(user_id=user.id).all()
    posts_num = Post.query.filter_by(user_id=user.id).count()
    return render_template("specific-user.html", title=f"{user.username}'s Page", user=user,
                           posts=posts, posts_num=posts_num)


@app.route("/all-posts/")
def all_posts():
    posts = Post.query.order_by(desc("date_posted")).all()
    posts_num = Post.query.count()
    return render_template("all-posts.html", title="Posts", posts=posts, posts_num=posts_num)


@app.route("/all-posts/asc")
def all_posts_asc():
    posts = Post.query.order_by("date_posted").all()
    posts_num = Post.query.count()
    return render_template("all-posts-asc.html", title="Posts", posts=posts, posts_num=posts_num)


@app.route("/all-posts/paginated/")
def all_posts_paginated():
    page = request.args.get("page", default=1, type=int)
    posts = Post.query.order_by(desc("date_posted")).paginate(per_page=10, page=page)
    posts_num = Post.query.count()
    return render_template("all-posts-paginated.html", posts=posts, posts_num=posts_num)


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def post_new():
    post_form = PostForm()
    if post_form.validate_on_submit():
        post = Post(title=post_form.title.data, content=post_form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created :3", "success")
        return redirect(url_for("post_view", id=post.id))
    return render_template("post-new.html", title="New Post", post_form=post_form)


@app.route("/post/<int:id>/modify", methods=["GET", "POST"])
@login_required
def post_modify(id):
    post = Post.query.get_or_404(id)
    if current_user == post.author:
        post_form = PostForm()

        if request.method == "GET":
            post_form.title.data = post.title
            post_form.content.data = post.content

        if post_form.validate_on_submit():
            post.title = post_form.title.data
            post.content = post_form.content.data
            post.date_modified_last = lambda: datetime.now(timezone.utc)
            db.session.commit()
            flash("Post's information has been modified", "info")
            return redirect(url_for("post_view", id=post.id))
        return render_template("post-modify.html", title=f"Modify '{post.title}'", post_form=post_form)
    else:
        flash("You are not the author of the post!", "danger")
        return redirect(url_for("post_view", id=post.id))


@app.route("/post/<int:id>/delete", methods=["POST"])
def post_delete(id):
    post = Post.query.get_or_404(id)
    post_author = post.author
    if current_user == post.author:
        db.session.delete(post)
        db.session.commit()
        flash("Post has been deleted", "info")
        return redirect(url_for("specific_user", id=post_author.id))
    else:
        flash("You are not the author of the post!", "danger")
        return redirect(url_for("post_view", id=post.id))


@app.route("/post/<int:id>")
def post_view(id):
    post = Post.query.get_or_404(id)
    return render_template("post-view.html", title=post.title, post=post)


@app.route("/all-posts/ideas")
def post_ideas():
    query = select(Post).where(Post.title.contains("#idea")).order_by(desc("date_posted"))
    posts = db.session.execute(query).scalars()

    posts_num = db.session.execute(query).scalars()
    # posts = Post.query.filter_by(title="#idea").all()
    b = 0
    for postik in posts_num:
        b += 1
    return render_template("all-posts-custom.html", posts=posts, legend="Ideas for the website",
                           title="Ideas", posts_num=b)


@app.route("/all-posts/programming")
def post_programming():
    query = select(Post).where(Post.title.contains("#programming")).order_by(desc("date_posted"))
    posts = db.session.execute(query).scalars()

    posts_num = db.session.execute(query).scalars()
    b = 0
    for postik in posts_num:
        b += 1
    return render_template("all-posts-custom.html", posts=posts, legend="Programming stuff",
                           title="Programming", posts_num=b)


@app.route("/all-posts/accomplishments")
def post_accomplishments():
    query = select(Post).where(Post.title.contains("#accomplishments")).order_by(desc("date_posted"))
    posts = db.session.execute(query).scalars()

    posts_num = db.session.execute(query).scalars()
    b = 0
    for postik in posts_num:
        b += 1
    return render_template("all-posts-custom.html", posts=posts, legend="Stuff I did during the session",
                           title="Accomplishments", posts_num=b)


@app.route("/all-posts/search/<string:searched_value>")
def search_result(searched_value:str):
    search_form = SearchForm()
    query_title = select(Post).where(Post.title.contains(searched_value)).order_by(desc("date_posted"))
    query_content = select(Post).where(Post.content.contains(searched_value)).order_by(desc("date_posted"))

    posts_title = db.session.execute(query_title).scalars()
    posts_content = db.session.execute(query_content).scalars()

    posts_title_num = db.session.execute(query_title).scalars()
    posts_content_num = db.session.execute(query_content).scalars()

    post_tit = 0
    post_cont = 0

    for postik in posts_title_num:
        post_tit += 1

    for postik in posts_content_num:
        post_cont += 1

    return render_template("all-posts-search.html", posts_title=posts_title, posts_content=posts_content,
                           post_title_num=post_tit, post_content_num=post_cont)


@app.route("/search_bar/", methods=["POST", "GET"])
def search_route():
    search_form = SearchForm()
    if search_form.bar.data:
        return redirect(url_for('search_result', searched_value=search_form.bar.data))
    return render_template("search.html", search_form=search_form)


