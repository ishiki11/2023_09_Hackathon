from flask import Flask, render_template, Blueprint
# from flask_migrate import Migrate
# databaseとの接続
from database import db
# viewsの読み込み
from views.auth import auth
from views.user_register import user_register
from views.todo_top import todo_top
from views.user_edit import user_edit
from views.user_logout import user_logout
# modelsの読み込み
from models import *
import string, random
from views.user_register import user_register
from views.user_edit import user_edit
from views.user_logout import user_logout
# インスタンスの生成
app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

# # configファイルの読み込み
# app.config.from_pyfile('config.py')
# # dbとの接続
# db.init_app(app)
# migrate = Migrate(app, db)

# Blueprintの利用
# 利用者auth
app.register_blueprint(auth)
app.register_blueprint(user_register)
app.register_blueprint(todo_top)
app.register_blueprint(user_edit)
app.register_blueprint(user_logout)


# Topページ
@app.route('/')
def index():
  return render_template('index.html')


if __name__ == '__main__':
  # デバッグモード有効
  app.debug = True
  # サーバー起動（ホスト名）
  app.run(host='localhost')
