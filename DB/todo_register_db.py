import os
import psycopg2


def get_connection():
  url = os.environ['DATABASE_URL']
  connection = psycopg2.connect(url)
  return connection


def todo_register(todo_inf):
  sql = "INSERT INTO ToDo VALUES (default, %s, %s, %s, 0, %s, %s, 0, %s)"
  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (todo_inf[0], todo_inf[1], todo_inf[2], todo_inf[3], todo_inf[4], todo_inf[5]))
    count = cursor.rowcount
    connection.commit()
  except psycopg2.DatabaseError:
    count = 0
  finally:
    cursor.close()
    connection.close()
    return count


def userMusic(userid):
  sql = "SELECT * FROM UserMusic JOIN Music on UserMusic.MusicId = Music.id where userId = %s"
  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (userid,))
    music = cursor.fetchall()
  except psycopg2.DatabaseError:
    music = "error"
  finally:
    cursor.close()
    connection.close()
    return music


def usermusic_search(user_id, music_id):
  sql = "SELECT * FROM usermusic WHERE userid = %s AND musicid = %s;"
  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (user_id, music_id,))
    music = cursor.fetchone()
  except psycopg2.DatabaseError:
    return music
  finally:
    cursor.close()
    connection.close()
    return music
