import os
import psycopg2


def get_connection():
  url = os.environ['DATABASE_URL']
  connection = psycopg2.connect(url)
  return connection


# 完了したtodoの取得
def todo_finished_list(userid):
  sql = "SELECT * FROM ToDo JOIN Music on ToDo.work_bgm = Music.id  WHERE user_id = %s AND comp_flg = 1"
  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (userid,))
    todo = cursor.fetchall()
  except psycopg2.DatabaseError:
    todo = "error"
  finally:
    cursor.close()
    connection.close()
    return todo


def todo_finished_break(userid):
  sql = "SELECT Music.title as break_title FROM ToDo JOIN music on ToDo.break_bgm = Music.id  WHERE user_id = %s AND comp_flg = 1"
  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (userid,))
    todo = cursor.fetchall()
  except psycopg2.DatabaseError:
    todo = "error"
  finally:
    cursor.close()
    connection.close()
    return todo
