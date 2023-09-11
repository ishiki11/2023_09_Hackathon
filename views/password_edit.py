from flask import render_template, Blueprint, request, redirect, session
import DB.user_edit_db as db
import re

password_edit = Blueprint('password_edit', __name__, '/password_edit')


# 編集処理
@password_edit.route('/password_edit')
def pass_edit():
  user_id = session.get('id')
  if user_id is None:
    # ログインへ遷移
    return redirect('/')

  user = db.id_select_user(user_id)
  # 存在しないuserの時
  if user is None:
    return redirect('/')

  return render_template('password_edit.html', data=user)


@password_edit.route('/password_edit', methods=['POST'])
def pass_edit_exe():
  user_id = session.get('id')
  if user_id is None:
    # ログインへ遷移
    return redirect('/')
  pw = request.form.get('pw', type=str)
  pw2 = request.form.get('pw2', type=str)

  error = ""
  # 入力がされていない項目がある場合
  user = db.id_select_user(user_id)
  if pw == "" or pw2 == "":
    error = "パスワードを入力して下さい"

  # 入力値チェック
  if len(pw) > 255:  # 文字数
    error = "入力文字数が多すぎます"

  # パスワードチェック
  if pw != pw2:  # pwとpw2が一致しないとき
    error = 'パスワードが一致していません'
  if len(pw) < 4:  # pw文字数チェック
    error = 'パスワートを4文字以上にしてください'
  if not re.search("[a-z]", pw) or not re.search("[A-Z]", pw):
    error = 'パスワードで大文字と小文字を使用してください'
  if not re.match("^[a-zA-Z0-9]+$", pw):
    error = 'パスワードは英数字のみを使用してください'

  old = [pw, pw2]

  # エラーがある時
  if error != "":
    return render_template("password_edit.html", error=error, old=old, data=user)

  flg = db.update_password(user_id, pw)
  if flg:
    msg = '変更が完了しました。'
    return render_template('password_edit.html', msg=msg, data=user)
  else:
    error = '変更出来ませんでした'
    return render_template('password_edit.html', error=error, old=old, data=user)
