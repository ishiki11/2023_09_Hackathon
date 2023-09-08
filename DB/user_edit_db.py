import os, psycopg2, string, random, hashlib
#trackと同じ

# DBへのコネクションを生成
def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection


def id_select_user(id):
    row=None
    sql = 'SELECT mail,username FROM Users where id = %s'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (id,))
        row =cursor.fetchone()

    except psycopg2.DatabaseError as e: # Java でいうcatch 失敗した時の処理をここに書く
        print(e)
        count = 0 # 例外が発生したら0 をreturn する。

    finally: # 成功しようが、失敗しようが、close する。
        cursor.close()
        connection.close()
    return row


def update_user(id, mail, pw, username):
    count=-1
    sql = 'UPDATE Users SET mail = %s, hashed_password = %s, username = %s WHERE id = %s'

    try:
        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(sql, (mail, pw, username, id))

        count = cursor.rowcount


        connection.commit()

    except psycopg2.DatabaseError as e:
        print(e)
        count = 0
    finally:
        cursor.close()
        connection.close()

    return count
