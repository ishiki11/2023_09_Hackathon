from flask import Blueprint, render_template, redirect, url_for, request, session
import re
import DB.todo_register_db as db

todo_reg = Blueprint('todo_reg', __name__)


@todo_reg.route('/todo_register', methods=['GET'])
def todo_register():
  user_id = session.get('id')
  # 後で消す
  if user_id is None:
    # ログインへ遷移
    return redirect('/')
  music = db.userMusic(user_id)
  return render_template('todo_register.html', music=music)


@todo_reg.route('/todo_register',  methods=['POST'])
def todo_register_exe():
  user_id = session.get('id')
  error = ""
  # 後で消す
  if user_id is None:
    # ログインへ遷移
    return redirect('/')
  task = request.form.get('task', type=str)
  target_time = request.form.get('target_time', type=str)
  work_bgm = request.form.get('work_bgm', type=int)
  break_bgm = request.form.get('break_bgm', type=int)
  priority = request.form.get('priority', type=int)
  todo_inf = [user_id, task, target_time, work_bgm, break_bgm, priority]
  print(todo_inf)
  # 入力値チェック
  if len(task) > 255 | len(target_time) > 255:
    # 文字数
    error = "入力文字数が多すぎます"

  if db.usermusic_search(user_id, work_bgm) is None or\
          db.usermusic_search(user_id, break_bgm) is None:
    # usermusicにある音楽を選択しているか
    error = "音楽を正しく設定してください"

  if priority != 0 and priority != 1 and priority != 2:
    # 優先度が0、1，2で設定されているか
    error = "優先度を正しく設定してください"

  time_pattern = re.compile(r'(^[1-9]\d?時間[1-9]\d?分$)|(^[1-9]\d?時間$)|(^[1-9]\d?分$)')
  if not time_pattern.match(target_time):
    # 正規表現パターン　受け付ける00時間00分　時間のみ分のみでも通る
    error = "目標時間を正しく設定してください 例：○時間○○分、○時間、○○分"

  # 入力値が空の時
  if task == "" or target_time == "" or work_bgm == "" or break_bgm == "" or priority == "":
    error = "入力されていない値があります"

  music = db.userMusic(user_id)
  # エラーがある時
  if error != "":
    return render_template('todo_register.html', error=error, music=music, old=todo_inf)  # oldは選択状態

  count = db.todo_register(todo_inf)
  if count == 1:
    return redirect(url_for('todo_top.todo_list'))
  else:
    error = '登録に失敗しました。'
    music = db.userMusic(user_id)
    return render_template('todo_register.html', error=error, music=music, old=todo_inf)  # oldは選択状態
