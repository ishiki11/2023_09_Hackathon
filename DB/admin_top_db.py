from sqlalchemy import text
import os
import psycopg2


# DBへのコネクションを生成
def get_connection():
  url = os.environ['DATABASE_URL']
  connection = psycopg2.connect(url)
  return connection


# todoの更新
def get_users():
  sql = "SELECT id, username, rank_rate, mail FROM users order by id"

  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    users = cursor.fetchall()
  except psycopg2.DatabaseError as e:
    raise Exception(e)
  finally:
    cursor.close()
    connection.close()
  return users


# 検索結果表示
def get_search_user(username):
  sql = "SELECT id, username, rank_rate, mail FROM users WHERE username LIKE %s ORDER BY id"

  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, ('%' + username + '%',))
    connection.commit()
    user = cursor.fetchall()
  except psycopg2.DatabaseError as e:
    raise Exception(e)
  finally:
    cursor.close()
    connection.close()
  return user


# ユーザの削除
def delete_user(user_id):
  sql = "DELETE FROM users WHERE id = %s"

  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (user_id,))
    connection.commit()
  except psycopg2.DatabaseError as e:
    raise Exception(e)
  finally:
    cursor.close()
    connection.close()
