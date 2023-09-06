from flask import Flask, Blueprint, render_template, redirect, url_for, request
import os, psycopg2
todo_edit= Blueprint('todo_edit', __name__)

@todo_edit.route('/todo_editer', methods=['GET'])
def todo_editer():
  userid = 1 #セッションで持ってくる
  todoId = request.form.get('todoid')
  music = userMusic(userid)
  todo = todo_search(todoId)
  return render_template('todo_edit.html', music=music)
def todo_edit_exe():
  userid = 1 #セッションで持ってくる
  task = request.form.get('task')
  target_time = request.form.get('target_time')
  work_bgm = request.form.get('work_bgm')
  break_bgm = request.form.get('break_bgm')
  priority = request.form.get('priority')
  todo_inf = [userid,task,target_time,work_bgm,break_bgm,priority]
  count = todo_edit_exe(todo_inf)
  if count == 1:
    return redirect(url_for('todo_top'))
  else:
    error = '登録に失敗しました。'
    music = userMusic(userid)
    return render_template('todo_register.html', error=error, music=music)

def todo_search(todoid):
  sql = "SELECT * FROM ToDo id = %s"
  try:
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    cursor = connection.cursor()
    cursor.execute(sql,(todoid,))
    todo = cursor.fetchall()
  except psycopg2.DatabaseError :
    todo = "error"
  finally :
    cursor.close()
    connection.close()
    return todo
def userMusic(userid):
  sql = "SELECT * FROM UserMusic JONI Music on UserMusic.MusicId = Music.id where userId = %s"
  try:
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    cursor = connection.cursor()
    cursor.execute(sql,(userid,))
    music = cursor.fetchall()
  except psycopg2.DatabaseError :
    music = "error"
  finally :
    cursor.close()
    connection.close()
    return music
