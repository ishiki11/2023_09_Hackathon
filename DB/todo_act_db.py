import os
import psycopg2


# DBへのコネクションを生成
def get_connection():
  url = os.environ['DATABASE_URL']
  connection = psycopg2.connect(url)
  return connection


# todoのdataを取得する
def get_todo(todo_id):
  sql = 'SELECT * FROM todo WHERE id = %s AND comp_flg = 0'

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
