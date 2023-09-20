from flask import Flask, Blueprint, render_template, session, redirect
import os
import psycopg2

mranking = Blueprint('mranking', __name__)


@mranking.route('/music_ranking', methods=['GET'])
def music_ranking():
  user_id = session.get('id')
  if user_id is None:
    # ログインへ遷移
    return redirect('/')
  try:
    work_ranking = workbgm_rank()
    break_ranking = breakbgm_rank()
  except Exception as e:
    print(e)
  count = 1
  rank_num = 1
  work_rank = []
  for wrank in work_ranking:
    if count == 1:
      work_rank.append([rank_num, wrank[0], wrank[1]])
    elif work_ranking[count-2][1] == wrank[1]:
      work_rank.append([rank_num, wrank[0], wrank[1]])
    else:
      rank_num = count
      work_rank.append([rank_num, wrank[0], wrank[1]])
    count += 1
  count = 1
  rank_num = 1
  break_rank = []
  for brank in break_ranking:
    if count == 1:
      break_rank.append([rank_num, brank[0], brank[1]])
    elif break_ranking[count-2][1] == brank[1]:
      break_rank.append([rank_num, brank[0], brank[1]])
    else:
      rank_num = count
      break_rank.append([rank_num, brank[0], brank[1]])
    count += 1
  return render_template('music_ranking.html', work_rank=work_rank, break_rank=break_rank)


def workbgm_rank():
  sql = "SELECT m.title, count(t.work_bgm) AS count FROM todo AS t Join Music AS m on t.work_bgm = m.id GROUP BY m.title ORDER BY count DESC limit 10"
  connection = None
  cursor = None
  try:
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    cursor = connection.cursor()
    cursor.execute(sql)
    myrank = cursor.fetchall()
  except psycopg2.DatabaseError as e:
    raise Exception(e)
  finally:
    if cursor:
      cursor.close()
    if connection:
      connection.close()
  return myrank


def breakbgm_rank():
  sql = "SELECT m.title, count(t.break_bgm) AS count FROM todo AS t Join Music AS m on t.break_bgm = m.id GROUP BY m.title ORDER BY count DESC limit 10"
  connection = None
  cursor = None
  try:
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    cursor = connection.cursor()
    cursor.execute(sql)
    myrank = cursor.fetchall()
  except psycopg2.DatabaseError as e:
    raise Exception(e)
  finally:
    if cursor:
      cursor.close()
    if connection:
      connection.close()
  return myrank
