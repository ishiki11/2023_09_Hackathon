from flask import Flask, Blueprint, render_template, redirect, url_for, request
import os, psycopg2
todo_register = Blueprint('todo_register', __name__)


@todo_register.route('/todo_register', methods=['GET'])
def todo_register():
  userid = 1 #セッションで持ってくる
  music = userMusic(userid)
  return render_template('todo_register.html', music=music)
@todo_register.route('/todo_register_exe',  methods=['POST'])
def todo_register_exe():
  userid = 1 #セッションで持ってくる
  task = request.form.get('task')
  target_time = request.form.get('target_time')
  work_bgm = request.form.get('work_bgm')
  break_bgm = request.form.get('break_bgm')
  priority = request.form.get('priority')
  todo_inf = [userid,task,target_time,work_bgm,break_bgm,priority]
  count = todo_register(todo_inf)
  if count == 1:
    return redirect(url_for('todo_top'))
  else:
    error = '登録に失敗しました。'
    music = userMusic(userid)
    return render_template('todo_register.html', error=error, music=music)

def todo_register(todo_inf):
  sql = "INSERT INTO ToDo VALUES (default, %s, %s, %s, 0, %s, %s, 0, %s)"
  try:
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    cursor = connection.cursor()
    cursor.execute(sql, (todo_inf[0],todo_inf[1],todo_inf[2],todo_inf[3],todo_inf[4],todo_inf[5]))
    count = cursor.rowcount
    connection.commit()
  except psycopg2.DatabaseError:
    count = 0
  finally:
    cursor.close()
    connection.close()
    return count
def userMusic(userid):
  sql = "SELECT * FROM UserMusic JONI Music on UserMusic.MusicId = Music.id where userId = %s"
  try:
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    cursor = connection.cursor()
    cursor.execute(sql,(userid))
    music = cursor.fetchall()
  except psycopg2.DatabaseError :
    music = "error"
  finally :
    cursor.close()
    connection.close()
    return music
