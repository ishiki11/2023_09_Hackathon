from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
# viewsの読み込み
from views.auth import auth


# インスタンスの生成
app = Flask(__name__)
# # configファイルの読み込み
# app.config.from_pyfile('config.py')
# # dbとの接続
# db = SQLAlchemy(app)


# Blueprintの利用
# 利用者auth
app.register_blueprint(auth)


# Topページ
@app.route('/')
def index():
  return render_template('index.html')


if __name__ == '__main__':
  # デバッグモード有効
  app.debug = True
  # サーバー起動（ホスト名）
  app.run(host='localhost')
