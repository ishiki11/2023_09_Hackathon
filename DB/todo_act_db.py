import os
import psycopg2


# DBへのコネクションを生成
def get_connection():
  url = os.environ['DATABASE_URL']
  connection = psycopg2.connect(url)
  return connection


# todoのdataを取得する
def get_todo(todo_id):
  # タスク名、目標時間、bgmタイトル、ファイルpathの取得
  sql = "SELECT todo.task, todo.target_time, music_work.title AS work_bgm_title,music_work.music_file AS " \
        "work_bgm_file,music_break.title AS break_bgm_title, music_break.music_file AS break_bgm_file " \
        "FROM todo LEFT JOIN music AS music_work ON todo.work_bgm = music_work.id LEFT JOIN music AS music_break ON todo.break_bgm = music_break.id " \
        "where todo.id = %s;"

  try:  # sql実行
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (todo_id))
    todo = cursor.fetchone()

  except psycopg2.DatabaseError:  # catchの処理
    todo = "error"

  finally:
    cursor.close()
    connection.close()
    return todo
