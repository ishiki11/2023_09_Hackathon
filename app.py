from flask import Flask, render_template
from flask_migrate import Migrate
# databaseとの接続
from database import db
# viewsの読み込み
from views.auth import auth
from views.todo_top import todo_top
# modelsの読み込み
from models import *

# インスタンスの生成
app = Flask(__name__)
# configファイルの読み込み
app.config.from_pyfile('config.py')
# dbとの接続
db.init_app(app)
migrate = Migrate(app, db)

# Blueprintの利用
# 利用者auth
app.register_blueprint(auth)
app.register_blueprint(todo_top)


# Topページ
@app.route('/')
def index():
  return render_template('index.html')


if __name__ == '__main__':
  # デバッグモード有効
  app.debug = True
  # サーバー起動（ホスト名）
  app.run(host='localhost')
