from flask import Blueprint, render_template, session, redirect
import DB.todo_finished_db as db

todo_finished = Blueprint('todo_finished', __name__)


@todo_finished.route('/todo_finished_list', methods=['GET'])
def todo_finished_list():
  user_id = session.get('id')
  if user_id is None:
    # ログインへ遷移
    return redirect('/')
  todo = db.todo_finished_list(user_id)
  return render_template('todo_finished.html', todo=todo)
