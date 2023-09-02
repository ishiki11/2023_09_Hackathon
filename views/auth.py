from flask import Flask, Blueprint, render_template

auth = Blueprint('auth', __name__)


# ログイン処理
@auth.route('/login')
def login():
  return render_template('login.html')
