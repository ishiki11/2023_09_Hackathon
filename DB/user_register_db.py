import os, psycopg2, string, random, hashlib
from flask import session

# DBへのコネクションを生成
def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

# def get_salt():
# ランダムなソルトを生成
def get_salt():

# 文字列の候補(英大小文字+ 数字)
    charset = string.ascii_letters + string.digits

# charset からランダムに30文字取り出して結合
    salt = ''.join(random.choices(charset, k=30))
    return salt

# ソルトとPWからハッシュ値を生成
def get_hash(pw, salt):
    b_pw = bytes(pw, "utf-8")
    b_salt = bytes(salt, "utf-8")
    hashed_password = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 1000).hex()
    return hashed_password



# 1件のユーザを新規登録
def insert_user(mail, pw, username):
    sql = 'INSERT INTO Users VALUES (default, %s, %s, %s, %s, 0, 0)'

    salt = get_salt() # ソルトの生成
    hashed_password = get_hash(pw, salt) # 生成したソルトでハッシュ

    try : # 例外処理
        print("#insert_user")
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (mail, hashed_password, salt, username, ))
        count = cursor.rowcount # 更新件数を取得
        connection.commit()
        # lastrow_id = cursor.lastrowid
        # print(cursor.fetchone())
        # cursor.close()
        # connection.close()

        # usersテーブルの末尾の1件を取得する
        # TODO: 無駄に全件取得しているのでリファクタリングする
        # connection = get_connection()
        # cursor = connection.cursor()
        # cursor.execute("select * from users;")
        # print(cursor.fetchall()[-1])
        # user = cursor.fetchall()[-1]

    except psycopg2.DatabaseError as e: # Java でいうcatch 失敗した時の処理をここに書く
        print(e)
        count = 0 # 例外が発生したら0 をreturn する。

    finally: # 成功しようが、失敗しようが、close する。
        cursor.close()
        connection.close()

    return count


def insert_user_music(user_id):
    sql = 'INSERT INTO Usermusic VALUES (default, 1, %s),(default, 2, %s),(default, 3, %s)'

    try : # 例外処理
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (user_id, user_id, user_id,))
        connection.commit()

    except psycopg2.DatabaseError as e: # Java でいうcatch 失敗した時の処理をここに書く
        print(e)
        count = 0 # 例外が発生したら0 をreturn する。

    finally: # 成功しようが、失敗しようが、close する。
        cursor.close()
        connection.close()




def select_user(mail):
    id = None
    sql = 'SELECT id from users where mail= %s'
    try:

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(mail,))
        user =cursor.fetchone()
        if user:
            id = user[0]

    except psycopg2.DatabaseError as e: # Java でいうcatch 失敗した時の処理をここに書く
        print(e)
        count = 0 # 例外が発生したら0 をreturn する。

    finally: # 成功しようが、失敗しようが、close する。
        cursor.close()
        connection.close()
    return id
