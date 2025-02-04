from flask import Blueprint, abort
from bungee_gum import db, bcrypt, mail
from bungee_gum.posts.forms import (PostForm, SearchForm)
from flask import render_template, redirect, flash, url_for, request
from bungee_gum.models import Post, User
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import desc, asc, select
from datetime import datetime, timezone

posts = Blueprint("posts", __name__)


@posts.route("/all-posts/")
def all_posts():
    posts = Post.query.order_by(desc("date_posted")).all()
    posts_num = Post.query.count()
    return render_template("all-posts.html", title="Posts", posts=posts, posts_num=posts_num)


@posts.route("/all-posts/asc")
def all_posts_asc():
    posts = Post.query.order_by("date_posted").all()
    posts_num = Post.query.count()
    return render_template("all-posts-asc.html", title="Posts", posts=posts, posts_num=posts_num)


@posts.route("/all-posts/paginated/")
def all_posts_paginated():
    page = request.args.get("page", default=1, type=int)
    posts = Post.query.order_by(desc("date_posted")).paginate(per_page=10, page=page)
    posts_num = Post.query.count()
    return render_template("all-posts-paginated.html", posts=posts, posts_num=posts_num)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def post_new():
    post_form = PostForm()
    if post_form.validate_on_submit():
        post = Post(title=post_form.title.data, content=post_form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created :3", "success")
        return redirect(url_for("posts.post_view", id=post.id))
    return render_template("post-new.html", title="New Post", post_form=post_form)


@posts.route("/post/<int:id>/modify", methods=["GET", "POST"])
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
            post.date_modified_last = lambda: datetime.now(datetime.timezone.utc)
            db.session.commit()
            flash("Post's information has been modified", "info")
            return redirect(url_for("posts.post_view", id=post.id))
        return render_template("post-modify.html", title=f"Modify '{post.title}'", post_form=post_form)
    else:
        abort(403)


@posts.route("/post/<int:id>/delete", methods=["POST"])
def post_delete(id):
    post = Post.query.get_or_404(id)
    post_author = post.author
    if current_user == post.author:
        db.session.delete(post)
        db.session.commit()
        flash("Post has been deleted", "info")
        return redirect(url_for("users.specific_user", id=post_author.id))
    else:
        flash("You are not the author of the post!", "danger")
        return redirect(url_for("posts.post_view", id=post.id))


@posts.route("/post/<int:id>")
def post_view(id):
    post = Post.query.get_or_404(id)
    return render_template("post-view.html", title=post.title, post=post)


@posts.route("/all-posts/ideas")
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


@posts.route("/all-posts/programming")
def post_programming():
    query = select(Post).where(Post.title.contains("#programming")).order_by(desc("date_posted"))
    posts = db.session.execute(query).scalars()

    posts_num = db.session.execute(query).scalars()
    b = 0
    for postik in posts_num:
        b += 1
    return render_template("all-posts-custom.html", posts=posts, legend="Programming stuff",
                           title="Programming", posts_num=b)


@posts.route("/all-posts/accomplishments")
def post_accomplishments():
    query = select(Post).where(Post.title.contains("#accomplishments")).order_by(desc("date_posted"))
    posts = db.session.execute(query).scalars()

    posts_num = db.session.execute(query).scalars()
    b = 0
    for postik in posts_num:
        b += 1
    return render_template("all-posts-custom.html", posts=posts, legend="Stuff I did during the session",
                           title="Accomplishments", posts_num=b)


@posts.route("/all-posts/search/<string:searched_value>")
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
                           post_title_num=post_tit, post_content_num=post_cont, searched_value=searched_value)


@posts.route("/search_bar/", methods=["POST", "GET"])
def search_route():
    search_form = SearchForm()
    if search_form.bar.data:
        return redirect(url_for('posts.search_result', searched_value=search_form.bar.data))
    return render_template("search.html", search_form=search_form)

