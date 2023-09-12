from flask import Flask, render_template, session
# viewsの読み込み
from views.user_register import user_register
from views.todo_top import todo_top
from views.user_edit import user_edit
from views.user_register import user_register
from views.user_logout import user_logout
from views.todo_act import todo_act
from views.todo_register import todo_reg
from views.login import login
from views.todo_edit import todo_edit
from views.plize_list import plize_list
from views.todo_finished import todo_finished
from views.password_edit import password_edit
from views.user_ranking import ranking
# 関数のインポート
import string
import random
# インスタンスの生成
app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))


# 利用者auth
app.register_blueprint(user_edit)  # ユーザ編集
app.register_blueprint(password_edit)  # パスワード編集
app.register_blueprint(user_logout)  # ログアウト
app.register_blueprint(user_register)  # 新規登録
app.register_blueprint(todo_top)  # todo一覧
app.register_blueprint(todo_act)  # todo実行
app.register_blueprint(todo_reg)  # todo登録
app.register_blueprint(login)  # ログイン
app.register_blueprint(todo_edit)  # todo編集
app.register_blueprint(todo_finished)  # todo完了
app.register_blueprint(ranking)
app.register_blueprint(plize_list)


# セッションを初期化
@app.before_request
def before_request():
  session.modified = True


# Topページ
@app.route('/')
def index():
  return render_template('login.html')


if __name__ == '__main__':
  # デバッグモード有効
  app.debug = True

  # サーバー起動（ホスト名）
  app.run(host='localhost', debug=True)