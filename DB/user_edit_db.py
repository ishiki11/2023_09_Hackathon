import os
import psycopg2
import string
import random
import hashlib


# DBへのコネクションを生成
def get_connection():
  url = os.environ['DATABASE_URL']
  connection = psycopg2.connect(url)
  return connection


# ランダムなソルトを生成
def get_salt():
  # 文字列の候補(英大小文字+ 数字)
  charset = string.ascii_letters + string.digits
  # charset からランダムに30文字取り出して結合
  salt = ''.join(random.choices(charset, k=30))
  return salt


# ソルトとPWからハッシュ値を生成
def get_hash(pw, salt):
  b_pw = bytes(pw, "utf-8")
  b_salt = bytes(salt, "utf-8")
  hashed_password = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 1000).hex()
  return hashed_password


# idが一致するuserデータ取得
def id_select_user(user_id):
  sql = 'SELECT * FROM Users where id = %s'
  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (user_id,))
    user = cursor.fetchone()
  except psycopg2.DatabaseError as e:  # Java でいうcatch 失敗した時の処理をここに書く
    print(e)
  finally:  # 成功しようが、失敗しようが、close する。
    cursor.close()
    connection.close()
    return user


# ユーザ編集 名前、メール変更
def update_user(user_id, mail, username):
  sql = 'UPDATE Users SET mail = %s, username = %s WHERE id = %s'
  flg = False

  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (mail, username, user_id,))
    connection.commit()
  except psycopg2.DatabaseError as e:
    print(e)
  finally:
    flg = True
    cursor.close()
    connection.close()
    return flg




