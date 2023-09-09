from flask import Blueprint, render_template, session, redirect
import DB.todo_top_db as db

todo_top = Blueprint('todo_top', __name__)


@todo_top.route('/todo_list', methods=['GET'])
def todo_list():
  user_id = session.get('id')
  if user_id is None:
    # ログインへ遷移
    return redirect('/')
  user_name = db.get_username(user_id)  # user名取得
  todo = db.todo_list(user_id)  # user_idが一致するtodoの取得
  break_bgm = db.todo_break(user_id)  # user_idが一致する音楽の取得
  get_todo = [[]]*len(todo)
  for i in range(len(todo)):
    get_todo[i] = todo[i]+break_bgm[i]
  return render_template('todo_top.html', todo=get_todo, username=user_name)
