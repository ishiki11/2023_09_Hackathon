from flask import Flask, render_template, Blueprint, session
# viewsの読み込み
from views.user_register import user_register
from views.todo_top import todo_top
from views.todo_register import todo_reg
from views.login import login
from views.todo_edit import todo_edit
from views.todo_finished import todo_finished
import string, random
# インスタンスの生成
app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

# Blueprintの利用
app.register_blueprint(user_register)
app.register_blueprint(todo_top)
app.register_blueprint(todo_reg)
app.register_blueprint(login)
app.register_blueprint(todo_edit)
app.register_blueprint(todo_finished)


# Topページ
@app.route('/')
def index():
  return render_template('login.html')


if __name__ == '__main__':
  # デバッグモード有効
  app.debug = True

  # サーバー起動（ホスト名）
  app.run(host='localhost', debug=True)
