from flask import Blueprint, redirect, render_template, session
import DB.todo_act_db as db

# Blueprint登録
todo_act = Blueprint('todo_act', __name__)


# todo実行中処理
@todo_act.route('/todo_act/<param>', methods=['GET'])
def act(param):
  user_id = 1  # loginができたら消す
  # if (session['id'] != None):
  #   user_id = session['id']
  # else:
  #   return redirect('/login')

  todo = db.get_todo(todo_id=param, user_id=user_id)

  if (todo == "error"):
    return redirect('todo')  # todo一覧にリダイレクトする
  # テンプレートファイルのtodo_act.html
  return render_template(
      'todo_act.html',
      data=todo
  )


# # todo完了処理
# @todo_act.route('/todo/act-fin/<param>', methods=['GET'])
