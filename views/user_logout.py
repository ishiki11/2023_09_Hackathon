from flask import Flask, render_template, Blueprint, request, redirect, url_for, session
import string
import random
import DB.user_edit_db as db
user_logout = Blueprint('user_logout', __name__, '/user_logout')


@user_logout.route("/logout", methods=["GET"])
def logout():
  session.pop('id', None)
  return redirect("/")
