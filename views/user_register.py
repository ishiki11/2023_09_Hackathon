from flask import Flask, render_template, Blueprint,request, redirect, url_for, session
import string, random
import DB.user_register_db as db
user_register = Blueprint('user_register', __name__, '/user_register')


# ログイン処理
@user_register.route('/user_register')
def register():
  print("A")
  return render_template('user_register.html')


@user_register.route('/user_register2')
def register2():
  return render_template('user_register2.html')



@user_register.route('/register_exe', methods=['POST'])
def register_exe():
    username = request.form.get('username')
    mail = request.form.get('mail')
    pw = request.form.get('pw')

    if username == '' or pw == '' or mail == '':
        a = '入力されていない項目があります'
        return render_template('user_register.html',a=a)

    count = db.insert_user(mail, pw, username)
    print("session")
    id=db.select_user(mail)
    print(id)
    if count == 1:
        session["id"] = id
        return redirect('/user_edit')
        # return render_template('user_register.html')
    else:
        error='登録失敗'
        return render_template('user_register.html',error=error)




      # ページ遷移でしか登録失敗の画面を出せない
