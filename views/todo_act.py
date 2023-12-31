import json
import math
from flask import Blueprint, redirect, render_template, session, request, url_for
import DB.todo_act_db as db

# Blueprint登録
todo_act = Blueprint('todo_act', __name__)


# todo実行中処理
@todo_act.route('/todo_act/<int:param>', methods=['GET'])
def act(param):
  user_id = session.get('id')
  if user_id is None:
    # ログインへ遷移
    return redirect('/')

  todo = db.get_todo(param, user_id)

  if (todo == None):
    return redirect(url_for('todo_top.todo_list'))  # todo一覧にリダイレクトする
  # テンプレートファイルのtodo_act.html
  return render_template(
      'todo_act.html',
      data=todo
  )


# # todo完了処理
@todo_act.route('/todo_act', methods=['POST'])
def todo_update():
  user_id = session.get('id')
  if user_id is None:
    # 処理失敗
    return json.dumps({"flag": False})
  # データ情報
  data = json.loads(request.data)

  get_point = math.floor(data["seconds"] / 60)  # 1分　1ポイント
  db.finish_todo(get_point, data["todo_id"], user_id)  # todoテーブルの完了フラグ、獲得ポイントを更新する
  # 処理の成功
  return json.dumps({"flag": True})
