import os
import psycopg2


# DBへのコネクションを生成
def get_connection():
  url = os.environ['DATABASE_URL']
  connection = psycopg2.connect(url)
  return connection


# todoのdataを取得する
def get_todo(todo_id, user_id):
  # タスク名、目標時間、bgmタイトル、ファイルpathの取得
  sql = "SELECT todo.id, todo.task, todo.target_time, music_work.title AS work_bgm_title,music_work.music_file AS " \
        "work_bgm_file,music_break.title AS break_bgm_title, music_break.music_file AS break_bgm_file " \
        "FROM todo LEFT JOIN music AS music_work ON todo.work_bgm = music_work.id LEFT JOIN music AS music_break ON todo.break_bgm = music_break.id " \
        "where todo.id = %s and todo.user_id = %s;"

  try:  # sql実行
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (todo_id, user_id,))
    todo = cursor.fetchone()
  except psycopg2.DatabaseError as e:  # catchの処理
    print(e)
  finally:
    cursor.close()
    connection.close()
    return todo


# Todoの実行完了時の処理
def finish_todo(get_point, todo_id, user_id):
  update_todo(get_point, todo_id, user_id)  # todoの更新
  update_point(get_point, user_id)  # usersの更新


# todoの更新
def update_todo(get_point, todo_id, user_id, ):
  sql = "UPDATE todo SET comp_flg = 1, get_point = %s WHERE id = %s AND user_id = %s"

  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (get_point, todo_id, user_id,))
    connection.commit()
  except psycopg2.DatabaseError as e:
    print("Database error:", e)
  finally:
    cursor.close()
    connection.close()


# usersのrank_rateとpointの更新
def update_point(get_point, user_id):
  sql = "UPDATE users SET rank_rate = rank_rate + %s, point = point + %s WHERE id = %s"

  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (get_point, get_point, user_id,))
    connection.commit()
  except psycopg2.DatabaseError as e:
    print("Database error:", e)
  finally:
    cursor.close()
    connection.close()
