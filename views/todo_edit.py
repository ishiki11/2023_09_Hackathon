from flask import Flask, Blueprint, render_template, redirect, url_for, request
import os, psycopg2
todo_edit= Blueprint('todo_edit', __name__)

@todo_edit.route('/todo_editer/<param>', methods=['GET'])
def todo_editer(param):
  userid = 1 #セッションで持ってくる
  todoId = param
  music = userMusic(userid)
  todo = todo_search(todoId)
  return render_template('todo_edit.html', music=music, todo=todo)
@todo_edit.route('/todo_edit_exe/<param>',  methods=['POST'])
def todo_edit_exe(param):
  userid = 1 #セッションで持ってくる
  task = request.form.get('task')
  target_time = request.form.get('target_time')
  work_bgm = request.form.get('work_bgm')
  break_bgm = request.form.get('break_bgm')
  priority = request.form.get('priority')
  todoId = param
  edit_inf = [task,target_time,work_bgm,break_bgm,priority,todoId]
  count = todo_edit_exe(edit_inf)
  if count == 1:
    return redirect(url_for('todo_top'))
  else:
    error = '変更に失敗しました。'
    music = userMusic(userid)
    todo = todo_search(todoId)
    return render_template('todo_edit.html', error=error, music=music, todo=todo)

def todo_edit_exe(edit_info):
  sql = "UPDATE todo SET (task,target_time,work_bgm,break_bgm,priority)=(%s,%s,%s,%s,%s) where id = %s"
  try:
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    cursor = connection.cursor()
    cursor.execute(sql,(edit_info[0],edit_info[1],edit_info[2],edit_info[3],edit_info[4],edit_info[5]))
    count = cursor.rowcount
    connection.commit()
  except psycopg2.DatabaseError :
    count = 0
  finally :
    cursor.close()
    connection.close()
    return count
def todo_search(todoid):
  sql = "SELECT * FROM todo where id = %s"
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
  sql = "SELECT * FROM UserMusic JOIN Music on UserMusic.MusicId = Music.id where userId = %s"
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
