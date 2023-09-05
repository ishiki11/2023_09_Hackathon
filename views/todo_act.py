from flask import Blueprint, redirect, render_template
import DB.todo_act_db as db

# Blueprint登録
todo_act = Blueprint('todo_act', __name__)


# todo実行中処理
@todo_act.route('/todo/act/<param>', methods=['GET'])
def act(param):
  todo = db.get_todo(todo_id=param)
  print(todo)
  if (todo == "error"):
    return redirect('todo')  # todo一覧にリダイレクトする
  # テンプレートファイルのtodo_act.html
  return render_template(
      'todo_act.html',
      data=todo
  )
