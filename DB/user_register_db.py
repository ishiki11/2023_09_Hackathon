import os, psycopg2, string, random, hashlib

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
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (mail, hashed_password, salt, username))
        count = cursor.rowcount # 更新件数を取得
        connection.commit()

    except psycopg2.DatabaseError: # Java でいうcatch 失敗した時の処理をここに書く
        count = 0 # 例外が発生したら0 をreturn する。

    finally: # 成功しようが、失敗しようが、close する。
        cursor.close()
        connection.close()

    return count
