from flask import Flask, render_template, Blueprint,request, redirect, url_for, session
import string, random, re
import DB.user_edit_db as db
user_edit = Blueprint('user_edit', __name__, '/user_edit')


# ログイン処理
@user_edit.route('/user_edit')
def edit():
  user_id = session.get('id')
  if user_id is None:
    # ログインへ遷移
    return redirect('/')

  row = db.id_select_user(user_id)

  print(row)

  return render_template('user_edit.html',row=row)


@user_edit.route('/edit_exe', methods=['POST'])
def edit_exe():
  user_id = session.get('id')
  if user_id is None:
    # ログインへ遷移
    return redirect('/')
  mail = request.form.get('mail')
  pw = request.form.get('pw')
  pw2 = request.form.get('pw2')
  username = request.form.get('username')
  print(user_id,pw,mail,username)
  
  row = (mail, username)


  if username == '' or pw == '' or mail == '' or pw2 == '':
      a = '入力されていない項目があります'
      return render_template('user_edit.html',a=a,row=row)


  if pw != pw2:
      error = 'パスワードが一致していません'
      return render_template('user_edit.html', error=error,row=row)

  if len(pw) < 4:
    error = 'パスワートを4文字以上にしてください'
    return render_template('user_edit.html',error=error,row=row)

  if not re.search("[a-z]", pw) or not re.search("[A-Z]", pw):
    error = 'パスワードは大文字、小文字の英数字のみを使用してください'
    return render_template('user_edit.html',error=error,row=row)

  if not re.match("^[a-zA-Z0-9]+$", pw):
    error = 'パスワードは英数字のみを使用してください'
    return render_template('user_edit.html',error=error,row=row)

  if len(mail) > 255 or len(username) > 255 or len(pw) > 255:
  # 文字数
    error = "入力文字数が多すぎます"
    return render_template('user_register.html',error=error,row=row)


  count = db.update_user(user_id, mail, pw, username)

  row = db.id_select_user(user_id)

  print(count)
  if count == 1:
      msg = '変更が完了しました。'
      return render_template('user_edit.html',msg=msg,row=row)
  else:
      error = '変更出来ませんでした'
      return render_template('user_edit.html', error=error,row=row)
