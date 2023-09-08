from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
import DB.user_login as db

login = Blueprint('login', __name__)


#   if msg == None:
#     return render_template('login.html')
#   else:
#     return render_template('login.html', msg=msg)


@login.route('/login', methods=['POST'])
def login_exe():
  mailaddress = request.form.get('mailaddress')
  password = request.form.get('password')
  # ログイン判定
  if db.login(mailaddress, password):
    userid = db.userid_search(mailaddress)
    session['id'] = userid
    return redirect(url_for('todo_top.todo_list'))
  else:
    error = 'メールアドレスまたはパスワードが違います。'
    # dictで返すことでフォームの入力量が増えても可読性が下がらない。
    input_data = {'mailaddress': mailaddress, 'password': password}
    return render_template('login.html', error=error, data=input_data)


@login.route('/register')
def register_form():
  return redirect(url_for('user_register.user_register'))
