import os
import psycopg2
import string
import random
import hashlib


def get_connection():
  url = os.environ['DATABASE_URL']
  connection = psycopg2.connect(url)
  return connection


def get_salt():
  charset = string.ascii_letters + string.digits

  salt = ''.join(random.choices(charset, k=30))
  return salt


def get_hash(pw, salt):
  b_pw = bytes(pw, "utf-8")
  b_salt = bytes(salt, "utf-8")
  hashed_password = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 1000).hex()
  return hashed_password


def login(mailaddress, password):
  sql = 'SELECT hashed_password, salt FROM users WHERE mail = %s'
  flg = False

  try:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(sql, (mailaddress,))
    user = cursor.fetchone()

    if user != None:
      # SQLの結果からソルトを取得
      salt = user[1]

      # DBから取得したソルト + 入力したパスワード からハッシュ値を取得
      hashed_password = get_hash(password, salt)

      # 生成したハッシュ値とDBから取得したハッシュ値を比較する
      if hashed_password == user[0]:
        flg = True

  except psycopg2.DatabaseError:
    flg = False

  finally:
    cursor.close()
    connection.close()

  return flg


def userid_search(mail):
  sql = "SELECT id FROM users where mail = %s"
  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (mail,))
    userid = cursor.fetchone()[0]
  except psycopg2.DatabaseError:
    userid = "error"
  finally:
    cursor.close()
    connection.close()
    return userid
