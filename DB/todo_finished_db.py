import os
import psycopg2


def get_connection():
  url = os.environ['DATABASE_URL']
  connection = psycopg2.connect(url)
  return connection


# 完了したtodoの取得
def todo_finished_list(userid):
  sql = "SELECT * FROM ToDo WHERE user_id = %s AND comp_flg = 1 ORDER BY id ASC;"
  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (userid,))
    todo = cursor.fetchall()
  except psycopg2.DatabaseError as e:
    print(e)
  finally:
    cursor.close()
    connection.close()
    return todo
