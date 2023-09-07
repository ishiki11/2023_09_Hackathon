from flask import Flask, render_template, Blueprint,request, redirect, url_for, session
import string, random
import DB.user_edit_db as db
user_edit = Blueprint('user_edit', __name__, '/user_edit')


# ログイン処理
@user_edit.route('/user_edit')
def edit():
  # print("A")
  id = session['id']


  row = db.id_select_user(session['id'])



  #sessionの処理したい

  print(row)

  return render_template('user_edit.html',row=row)


@user_edit.route('/edit_exe', methods=['POST'])
def edit_exe():
    user_id = session['id']
    mail = request.form.get('mail')
    pw = request.form.get('pw')
    username = request.form.get('username')
    print(user_id,pw,mail,username)

    count = db.update_user(user_id, mail, pw, username)

    row = db.id_select_user(id)

    print(count)
    if count == 1:
        msg = '変更が完了しました。'
        return render_template('user_edit.html',msg=msg,row=row)
    else:
        error = '変更出来ませんでした'
        return render_template('user_edit.html', error=error,row=row)
