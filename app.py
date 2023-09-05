# パッケージのimport
from flask import Flask, render_template
# viewsの読み込み
from views.auth import auth
from views.user_register import user_register
from views.todo_top import todo_top
from views.todo_act import todo_act
# 関数のインポート
import string
import random

# インスタンスの生成
app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

# Blueprintの利用
app.register_blueprint(auth)
app.register_blueprint(user_register)  # 新規登録
app.register_blueprint(todo_top)  # todo一覧
app.register_blueprint(todo_act)  # todo実行


# Topページ
@app.route('/')
def index():
  return render_template('index.html')


if __name__ == '__main__':
  # デバッグモード有効
  app.debug = True
  # サーバー起動（ホスト名）
  app.run(host='localhost')
