from sqlalchemy import text
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


def get_unowned_music(user_id):
  sql = text("""
        SELECT m.id, m.title, m.music_file, m.music_point
        FROM Music m
        LEFT JOIN UserMusic um ON m.id = um.musicId AND um.userId = :user_id
        WHERE um.id IS NULL
    """)
  result = db.engine.execute(sql, user_id=user_id)
  return result
