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
  sql = "SELECT * FROM ToDo JOIN Music on ToDo.work_bgm = Music.id  WHERE user_id = %s AND comp_flg = 0"
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


# todoの音楽の取得
def todo_break(user_id):
  sql = "SELECT Music.title as break_title FROM ToDo JOIN music on ToDo.break_bgm = Music.id  WHERE user_id = %s AND comp_flg = 0"
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
