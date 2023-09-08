from flask import Flask, Blueprint, render_template
import os, psycopg2
todo_finished = Blueprint('todo_finished', __name__)


@todo_finished.route('/todo_finished_list', methods=['GET'])
def todo_finished_list():
  userid = 1 #セッションで持ってくる
  todo = todo_finished_list(userid)
  break_bgm = todo_finished_break(userid)
  get_todo=[[]]*len(todo)
  for i in range(len(todo)):
    get_todo[i]=todo[i]+break_bgm[i]
  return render_template('todo_finished',todo=get_todo)

def todo_finished_list(userid):
  sql = "SELECT * FROM ToDo JOIN Music on ToDo.work_bgm = Music.id  WHERE user_id = %s AND comp_flg = 1"
  try:
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    cursor = connection.cursor()
    cursor.execute(sql,(userid,))
    todo = cursor.fetchall()
  except psycopg2.DatabaseError :
    todo = "error"
  finally :
    cursor.close()
    connection.close()
    return todo
def todo_finished_break(userid):
  sql = "SELECT Music.title as break_title FROM ToDo JOIN music on ToDo.break_bgm = Music.id  WHERE user_id = 1 AND comp_flg = 1"
  try:
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    cursor = connection.cursor()
    cursor.execute(sql,(userid,))
    todo = cursor.fetchall()
  except psycopg2.DatabaseError :
    todo = "error"
  finally :
    cursor.close()
    connection.close()
    return todo
