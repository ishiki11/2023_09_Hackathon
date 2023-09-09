from flask import Blueprint, render_template, redirect, url_for, request, session
import DB.todo_edit_db as db
import re

todo_edit = Blueprint('todo_edit', __name__)


@todo_edit.route('/todo_editer/<param>', methods=['GET'])
def todo_editer(param):
  user_id = session.get('id')

  # 後で消す
  user_id = 1

  if user_id is None:
    # ログインへ遷移
    return redirect('/')

  try:
    todoId = int(param)
  except ValueError:
    # paramが数値じゃない時
    return redirect(url_for('todo_top.todo_list'))  # todo一覧に戻る

  music = db.userMusic(user_id)  # UserMusicテーブルの値を取得
  todo = db.todo_search(todoId)  # todo_idが一致するdata取得
  if todo is None:
    # todoが取得できない時todo_listに遷移
    return redirect(url_for('todo_top.todo_list'))
  return render_template('todo_edit.html', music=music, todo=todo)


@todo_edit.route('/todo_editer/<param>',  methods=['POST'])
def todo_editer_exe(param):
  user_id = session.get('id')

  # 後で消す
  user_id = 1

  if user_id is None:
    # ログインへ遷移
    return redirect('/')

  # 入力がない部分の値設定（データベースから）
  if param is None:
    return redirect(url_for('todo_top.todo_list'))  # todo一覧に戻る

  try:
    todoId = int(param)
  except ValueError:
    # paramが数値じゃない時
    return redirect(url_for('todo_top.todo_list'))  # todo一覧に戻る

  todo = db.todo_search(todoId)
  task = request.form.get('task', default=todo[2], type=str)
  target_time = request.form.get('target_time', default=todo[3], type=str)
  work_bgm = request.form.get('work_bgm', default=todo[5], type=int)
  break_bgm = request.form.get('break_bgm', default=todo[6], type=int)
  priority = request.form.get('priority', default=todo[8], type=int)

  # 値が空の時
  if task == "":
    task = todo[2]
  if target_time == "":
    target_time = todo[3]
  if work_bgm == "":
    work_bgm = todo[5]
  if work_bgm == "":
    work_bgm = todo[6]
  if work_bgm == "":
    work_bgm = todo[8]

  edit_inf = [task, target_time, int(work_bgm), int(break_bgm), int(priority), int(todoId)]

  # 正規表現パターン　受け付ける00時間00分　時間のみ分のみでも通る
  time_pattern = re.compile(r'^([1-9]\d?時間[1-9]\d?分)|([1-9]\d?時間)|([1-9]\d?分)$')

  music = db.userMusic(user_id)  # UserMusicテーブルの値を取得

  if not time_pattern.match(target_time):
    error = "目標時間を正しく設定してください 数字は半角のみです"
    return render_template('todo_edit.html', error=error, music=music, todo=todo)

  count = db.todo_edit_exe(edit_inf)
  if count == 1:
    return redirect(url_for('todo_top.todo_list'))  # todo一覧に戻る
  else:
    error = '変更に失敗しました。'
    music = db.userMusic(user_id)
    todo = db.todo_search(todoId)
    return render_template('todo_edit.html', error=error, music=music, todo=todo)
