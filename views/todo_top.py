from flask import Flask, Blueprint, render_template, session
import os
import psycopg2
todo_top = Blueprint('todo_top', __name__)


@todo_top.route('/todo_list', methods=['GET'])
def todo_list():
  if 'user' in session:
    userid = 1  # セッションで持ってくる
    todo = todo_list(userid)
    break_bgm = todo_break(userid)
    get_todo = [[]]*len(todo)
    for i in range(len(todo)):
      get_todo[i] = todo[i]+break_bgm[i]
    return render_template('todo_top.html', todo=get_todo)
  else:
    return render_template('login.html')


def todo_list(userid):
  sql = "SELECT * FROM ToDo JOIN Music on ToDo.work_bgm = Music.id  WHERE user_id = %s AND comp_flg = 0"
  try:
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    cursor = connection.cursor()
    cursor.execute(sql, (userid,))
    todo = cursor.fetchall()
  except psycopg2.DatabaseError:
    todo = "error"
  finally:
    cursor.close()
    connection.close()
    return todo


def todo_break(userid):
  sql = "SELECT Music.title as break_title FROM ToDo JOIN music on ToDo.break_bgm = Music.id  WHERE user_id = 1 AND comp_flg = 0"
  try:
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    cursor = connection.cursor()
    cursor.execute(sql, (userid,))
    todo = cursor.fetchall()
  except psycopg2.DatabaseError:
    todo = "error"
  finally:
    cursor.close()
    connection.close()
    return todo
