from flask import Flask, Blueprint, render_template
import os, psycopg2
todo_top = Blueprint('todo_top', __name__)


@todo_top.route('/todo_list', methods=['GET'])
def todo_list():
  todo = todo_list()
  return render_template('todo_top.html',todo=todo)

def todo_list():
  userid = 1 #セッションで持ってくる
  sql = "SELECT * FROM ToDo where user_id = %s AND comp_flg = 0"
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
