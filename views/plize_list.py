import os
import psycopg2
import string
import random
import hashlib
from flask import Blueprint, render_template, request

plize_list = Blueprint('plize_list', __name__)

# DBへのコネクションを生成


def get_connection():
  url = os.environ['DATABASE_URL']
  connection = psycopg2.connect(url)
  return connection

# ユーザーが所有していない音楽を取得


def get_unowned_music(user_id):
  sql = """
        SELECT m.id, m.title, m.music_file, m.music_point
        FROM Music m
        LEFT JOIN UserMusic um ON m.id = um.musicid AND um.userid = %s
        WHERE um.id IS NULL
    """
  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (user_id,))
    result = cursor.fetchall()
    return result
  except psycopg2.DatabaseError as e:
    print(e)
    return []


@plize_list.route('/purchase')
def purchase_music():
  # ユーザーIDを適切に取得する方法に置き換えてください
  user_id = 1  # ダミーユーザーID、実際のユーザーIDに置き換えてください

  # ユーザーが所有していない音楽を取得
  unowned_music = get_unowned_music(user_id)

  return render_template('plize_list.html', unowned_music=unowned_music)
