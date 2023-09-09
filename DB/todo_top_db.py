import os
import psycopg2


def get_connection():
  url = os.environ['DATABASE_URL']
  connection = psycopg2.connect(url)
  return connection


# user名取得
def get_username(user_id):
  sql = "SELECT username FROM users WHERE id = %s"
  try:
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    cursor = connection.cursor()
    cursor.execute(sql, (user_id,))
    user_name = cursor.fetchone()
  except psycopg2.DatabaseError as e:
    print(e)
  finally:
    cursor.close()
    connection.close()
    return user_name


# todoのリスト表示
def todo_list(user_id):
  sql = "SELECT t.id, t.user_id, t.task, t.target_time, t.get_point, t.work_bgm, t.break_bgm, t.comp_flg, t.priority, mw.title AS work_bgm_title, mb.title AS break_bgm_title " \
      "FROM ToDo AS t " \
      "JOIN Music AS mw ON t.work_bgm = mw.id JOIN Music AS mb ON t.break_bgm = mb.id WHERE user_id = %s AND comp_flg = 0 ORDER BY id DESC;"
  try:
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    cursor = connection.cursor()
    cursor.execute(sql, (user_id,))
    todo = cursor.fetchall()
  except psycopg2.DatabaseError as e:
    print(e)
  finally:
    cursor.close()
    connection.close()
    return todo
