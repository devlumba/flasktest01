from flask import Blueprint

from bungee_gum.users.forms import (RegistrationForm)
from flask import render_template, redirect, flash, url_for, request


main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("home.html", title="dInAmIcc tiTle")


@main.route("/test1/")
def test1():
    form = RegistrationForm()
    return render_template("test1.html", title="test1", form=form)


