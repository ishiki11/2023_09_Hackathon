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
