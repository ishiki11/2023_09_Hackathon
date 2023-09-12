from flask import Flask, Blueprint, render_template, session, redirect
import os, psycopg2
ranking = Blueprint('ranking', __name__)


@ranking.route('/user_ranking', methods=['GET'])
def user_ranking():
  user_id = session.get('id')
  if user_id is None:
  # ログインへ遷移
    return redirect('/')
  userrank = user_rank()
  myranking = myrank(user_id)
  print(myranking)
  print(userrank)
  count = 1
  rank_num = 1
  rank = []
  for urank in userrank:
    if count == 1:
      rank.append([rank_num,urank[0],urank[1]])
    elif userrank[count-2][1]== urank[1]:
      rank.append([rank_num,urank[0],urank[1]])
    else:
      rank_num = count
      rank.append([rank_num,urank[0],urank[1]])
    count+=1
  return render_template('user_ranking.html',rank=rank,myrank=myranking)


def user_rank():
  sql = "SELECT username, rank_rate FROM Users WHERE rank_rate > 0 ORDER BY rank_rate DESC LIMIT 10;"
  connection = None
  cursor = None
  try:
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    cursor = connection.cursor()
    cursor.execute(sql,)
    rank = cursor.fetchall()
  except psycopg2.DatabaseError as e:
    rank = e
  finally :
    if cursor:
      cursor.close()
    if connection:
      connection.close()
  return rank


def myrank(userid):
  sql = "SELECT rank_rate FROM Users where id = %s"
  connection = None
  cursor = None
  try:
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    cursor = connection.cursor()
    cursor.execute(sql, (userid,))
    myrank = cursor.fetchall()
  except psycopg2.DatabaseError as e:
    myrank = e
  finally :
    if cursor:
      cursor.close()
    if connection:
      connection.close()
  return myrank