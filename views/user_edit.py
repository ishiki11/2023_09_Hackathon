from flask import render_template, Blueprint, request, redirect, session
import DB.user_edit_db as db

user_edit = Blueprint('user_edit', __name__, '/user_edit')


# 編集処理
@user_edit.route('/user_edit')
def edit():
  user_id = session.get('id')
  if user_id is None:
    # ログインへ遷移
    return redirect('/')

  user = db.id_select_user(user_id)
  # 存在しないuserの時
  if user is None:
    return redirect('/')

  return render_template('user_edit.html', data=user)


@user_edit.route('/user_edit', methods=['POST'])
def edit_exe():
  user_id = session.get('id')
  error = ""
  if user_id is None:
    # ログインへ遷移
    return redirect('/')
  mail = request.form.get('mail', type=str)
  username = request.form.get('username', type=str)

  # 入力がされていない項目がある場合
  user = db.id_select_user(user_id)
  if mail == "":
    mail = user[1]
  if username == "":
    username = user[4]

  # 入力値チェック
  if len(mail) > 255 or len(username) > 255:  # 文字数
    error = "入力文字数が多すぎます"
    print(error)

  # 値保持
  old = [mail, username]

  # エラーがある時
  if error != "":
    return render_template("user_edit.html", error=error, old=old, data=user)

  flg = db.update_user(user_id, mail, username)
  if flg:
    msg = '変更が完了しました'
    # 変更後のdata表示
    user = db.id_select_user(user_id)
    return render_template('user_edit.html', msg=msg, data=user)
  else:
    error = '変更出来ませんでした'
    return render_template('user_edit.html', error=error, old=old, data=user)
