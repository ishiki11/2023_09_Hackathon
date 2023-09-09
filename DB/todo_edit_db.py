import os
import psycopg2


def get_connection():
  url = os.environ['DATABASE_URL']
  connection = psycopg2.connect(url)
  return connection


# todo編集
def todo_edit_exe(edit_info):
  sql = "UPDATE todo SET (task,target_time,work_bgm,break_bgm,priority)=(%s,%s,%s,%s,%s) where id = %s"
  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (edit_info[0], edit_info[1], edit_info[2], edit_info[3], edit_info[4], edit_info[5]))
    count = cursor.rowcount
    connection.commit()
  except psycopg2.DatabaseError:
    count = 0
  finally:
    cursor.close()
    connection.close()
    return count


# todo検索
def todo_search(todoid):
  sql = "SELECT * FROM todo where id = %s"
  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (todoid,))
    todo = cursor.fetchall()
  except psycopg2.DatabaseError:
    todo = "error"
  finally:
    cursor.close()
    connection.close()
    return todo


def userMusic(user_id):
  sql = "SELECT * FROM UserMusic JOIN Music on UserMusic.MusicId = Music.id where userId = %s"
  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (user_id,))
    music = cursor.fetchall()
  except psycopg2.DatabaseError:
    music = "error"
  finally:
    cursor.close()
    connection.close()
    return music
