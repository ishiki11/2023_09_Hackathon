from flask import Flask, render_template
# viewsの読み込み
from auth import user_auth

# インスタンスの生成
app = Flask(__name__)

# CRUD操作
app.register_blueprint(user_auth)


# Topページ
@app.route('/')
def index():
  return render_template('index.html')


if __name__ == '__main__':
  # デバッグモード有効
  app.debug = True
  # サーバー起動（ホスト名）
  app.run(host='localhost')
