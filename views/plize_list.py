# plize_list.py
import os
import psycopg2
from flask import Blueprint, render_template, request, session, redirect, url_for, redirect

plize_list = Blueprint('plize_list', __name__)

def get_music_price(music_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql = "SELECT music_point FROM Music WHERE id = %s"
        cursor.execute(sql, (music_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return 0  # 音楽が存在しない場合は価格0とする
    except psycopg2.DatabaseError as e:
        print(e)
        return 0

def update_user_points(user_id, updated_points):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        # ユーザーのポイントを更新するSQLクエリを実行
        sql = "UPDATE Users SET point = %s WHERE id = %s"
        cursor.execute(sql, (updated_points, user_id))
        connection.commit()
    except psycopg2.DatabaseError as e:
        print(e)
    finally:
        cursor.close()
        connection.close()

def add_user_music(user_id, music_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        # UserMusic テーブルに音楽の所有情報を追加するSQLクエリを実行
        sql = "INSERT INTO UserMusic (musicId, userId) VALUES (%s, %s)"
        cursor.execute(sql, (music_id, user_id))
        connection.commit()
    except psycopg2.DatabaseError as e:
        print(e)
    finally:
        cursor.close()
        connection.close()
def get_user_points(user_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql = "SELECT point FROM Users WHERE id = %s"
        cursor.execute(sql, (user_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return 0  # ユーザーが存在しない場合はポイント0とする
    except psycopg2.DatabaseError as e:
        print(e)
        return 0
    finally:
        cursor.close()
        connection.close()
def check_user_owns_music(user_id, music_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql = "SELECT id FROM UserMusic WHERE userId = %s AND musicId = %s"
        cursor.execute(sql, (user_id, music_id))
        result = cursor.fetchone()
        return result is not None  # レコードが存在すればTrueを返す
    except psycopg2.DatabaseError as e:
        print(e)
        return False
    finally:
        cursor.close()
        connection.close()


# 以下省略

# DBへのコネクションを生成
def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

# ユーザーが所有していない音楽を取得
def get_unowned_music(user_id):
    sql = """
        SELECT m.id, m.title, m.music_file, m.music_point
        FROM Music m
        LEFT JOIN UserMusic um ON m.id = um.musicId AND um.userId = %s
        WHERE um.id IS NULL
    """
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (user_id,))
        result = cursor.fetchall()
        return result
    except psycopg2.DatabaseError as e:
        print(e)
        return []

@plize_list.route('/purchase')
def purchase_music_view():
    user_id = session.get('id')
    if user_id is None:
        return redirect('/')
    user_points = get_user_points(user_id)
    if "message" in session:
        message = session["message"]
    else:
        message = ""

    # ユーザーが所有していない音楽を取得
    unowned_music = get_unowned_music(user_id)

    return render_template('plize_list.html', unowned_music=unowned_music,user_points=user_points, message=message)

@plize_list.route('/purchase/<int:music_id>', methods=['POST'])
def purchase_music(music_id):
    # ユーザーIDを適切に取得する方法に置き換えてください
    user_id = session.get('id')
        
    if user_id is None:
        return redirect('/')

    # 音楽の価格を取得
    music_price = get_music_price(music_id)  # 適切な関数を作成して音楽の価格を取得してください

    # ユーザーが所有していない音楽を取得
    unowned_music = get_unowned_music(user_id)

    # ユーザーが既にその音楽を所有しているかチェック
    if check_user_owns_music(user_id, music_id):
        session["message"]="既に所有している音楽です"
        return redirect((url_for('plize_list.purchase_music_view')))
        # ユーザーの現在のポイントを取得
    user_points = get_user_points(user_id)

    # ユーザーのポイントが音楽の価格以上かチェック
    if user_points >= music_price:
        # ポイントを減算
        updated_points = user_points - music_price
        update_user_points(user_id, updated_points)  # ユーザーのポイントを更新する関数を作成してください

        # UserMusicテーブルに音楽の所有情報を追加
        add_user_music(user_id, music_id)  # ユーザーが音楽を所有する関数を作成してください
        try:
            music_name = get_music_name(music_id)
        except psycopg2.DatabaseError as e:
            print(e)
        finally :
            session["message"]=music_name[0][0]+"を購入しました"

    else:
        session["message"]="ポイントが不足しています"
    return redirect(url_for('plize_list.purchase_music_view'))


    # ユーザーが所有していない音楽を取得する関数
def get_unowned_music(user_id):
    sql = """
        SELECT m.id, m.title, m.music_file, m.music_point
        FROM Music m
        LEFT JOIN UserMusic um ON m.id = um.musicId AND um.userId = %s
        WHERE um.id IS NULL
    """
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (user_id,))
        result = cursor.fetchall()
        return result
    except psycopg2.DatabaseError as e:
        print(e)
        return []

def get_music_name(music_id):
  sql = "SELECT title FROM Music where id = %s"
  connection = None
  cursor = None
  try:
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    cursor = connection.cursor()
    raise Exception('例外のテスト')
    cursor.execute(sql, (music_id,))
    title = cursor.fetchall()
  except Exception as e:
    title = e
  finally :
    if cursor:
      cursor.close()
    if connection:
      connection.close()
  return title