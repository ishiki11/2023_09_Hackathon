from flask import Flask, Blueprint, render_template
import os, psycopg2
ranking = Blueprint('ranking', __name__)


@ranking.route('/user_ranking', methods=['GET'])
def user_ranking():
  userid = 1 #セッションで持ってくる
  myranking = myrank(userid)
  print(myranking)
  userrank = user_rank()
  count = 1
  rank_num = 1
  rank = []
  print(userrank)
  for urank in userrank:
    if count == 1:
      rank.append([rank_num,urank[0],urank[1]])
    elif userrank[count-2][1] == urank[1]:
      rank.append([rank_num,urank[0],urank[1]])
    else:
      rank_num = count
      rank.append([rank_num,urank[0],urank[1]])
  count+=1
  return render_template('user_ranking.html',rank=rank,myrank=myranking)
def user_rank():
  sql = "SELECT username, rank_rate FROM Users ORDER BY rank_rate DESC LIMIT 10;"
  try:
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    cursor = connection.cursor()
    cursor.execute(sql,)
    rank = cursor.fetchall()
  except psycopg2.DatabaseError :
    rank = "error"
  finally :
    cursor.close()
    connection.close()
    return rank
def myrank(userid):
  sql = "SELECT rank_rate FROM Users where id = %s"
  try:
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    cursor = connection.cursor()
    cursor.execute(sql,(userid,))
    myrank = cursor.fetchone()
  except psycopg2.DatabaseError :
    myrank = "error"
  finally :
    cursor.close()
    connection.close()
    return myrank