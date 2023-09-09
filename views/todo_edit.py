from flask import Blueprint, render_template, redirect, url_for, request, session
import DB.todo_edit_db as db

todo_edit = Blueprint('todo_edit', __name__)


@todo_edit.route('/todo_editer/<param>', methods=['GET'])
def todo_editer(param):
  user_id = session.get('id')
  if user_id is None:
    # ログインへ遷移
    return redirect('/')
  music = db.userMusic(user_id)
  todoId = param
  todo = db.todo_search(todoId)  # todo_idが一致するdata取得
  return render_template('todo_edit.html', music=music, todo=todo)


@todo_edit.route('/todo_editer',  methods=['POST'])
def todo_edit_exe(param):
  user_id = session.get('id')
  if user_id is None:
    # ログインへ遷移
    return redirect('/')
  task = request.form.get('task')
  target_time = request.form.get('target_time')
  work_bgm = request.form.get('work_bgm')
  break_bgm = request.form.get('break_bgm')
  priority = request.form.get('priority')
  todoId = param
  edit_inf = [task, target_time, work_bgm, break_bgm, priority, todoId]
  count = db.todo_edit_exe(edit_inf)
  if count == 1:
    return redirect(url_for('todo_top.todo_list'))
  else:
    error = '変更に失敗しました。'
    music = db.userMusic(user_id)
    todo = db.todo_search(todoId)
    return render_template('todo_edit.html', error=error, music=music, todo=todo)
