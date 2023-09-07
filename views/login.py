from flask import Flask, Blueprint, render_template, request, redirect, url_for
import db

login = Blueprint('login', __name__)
app = Flask(__name__)

# ログイン処理
@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')

    if msg == None:
        return render_template('login.html')
    else :
        return render_template('login.html', msg=msg)

@app.route('/', methods=['POST'])
def login_exe():
    mailaddress = request.form.get('mailaddress')
    password = request.form.get('password')

    # ログイン判定
    if db.login(mailaddress, password):
        return redirect(url_for('mypage'))
    else :
        error = 'メールアドレスまたはパスワードが違います。'

        # dictで返すことでフォームの入力量が増えても可読性が下がらない。
        input_data = {'mailaddress':mailaddress, 'password':password}
        return render_template('login.html', error=error, data=input_data)

@app.route('/mypage', methods=['GET'])
def mypage():
    return render_template('mypage.html')

@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    mailaddress = request.form.get('mailaddress')
    password = request.form.get('password')

    if mailaddress == '':
        error = 'メールアドレスが未入力です。'
        return render_template('register.html', error=error, mailaddress=mailaddress, password=password)
    if password == '':
        error = 'パスワードが未入力です。'
        return render_template('register.html', error=error)

    count = db.insert_user(mailaddress, password)

    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('register.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)