from flask import render_template, Blueprint, request, redirect, session
import re
import DB.user_register_db as db


user_register = Blueprint('user_register', __name__, '/user_register')


# ログイン処理
@user_register.route('/user_register')
def register():
  return render_template('user_register.html')


@user_register.route('/user_register2')
def register2():
  return render_template('user_register2.html')


@user_register.route('/register_exe', methods=['POST'])
def register_exe():
  mail = request.form.get('mail')
  pw = request.form.get('pw')
  pw2 = request.form.get('pw2')
  username = request.form.get('username')

  if username == '' or pw == '' or mail == '':
    a = '入力されていない項目があります'
    return render_template('user_register.html', a=a)

  if pw != pw2:
    error = 'パスワードが一致していません'
    return render_template('user_register.html', error=error)

  if len(pw) < 4:
    error = 'パスワートを4文字以上にしてください'
    return render_template('user_register.html', error=error)

  if not re.search("[a-z]", pw) or not re.search("[A-Z]", pw):
    error = 'パスワードで大文字と小文字を使用してください'
    return render_template('user_register.html', error=error)

  if not re.match("^[a-zA-Z0-9]+$", pw):
    error = 'パスワードは英数字のみを使用してください'
    return render_template('user_register.html', error=error)

  if len(mail) > 255 or len(username) > 255 or len(pw) > 255:
    # 文字数
    error = "入力文字数が多すぎます"
    return render_template('user_register.html', error=error)

  count = db.insert_user(mail, pw, username)
  id = db.select_user(mail)
  if count == 1:
    session["id"] = id
    db.insert_user_music(id)
    return redirect('/todo_list')
  else:
    error = '登録失敗'
    return render_template('user_register.html', error=error)
