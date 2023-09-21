from flask import Blueprint, render_template, request, redirect, session, json
import DB.admin_top_db as db

admin_top = Blueprint('admin_top', __name__)


# トップ画面表示
@admin_top.route('/admin/top', methods=['GET'])
def user_list():
  try:
    users = db.get_users()
  except Exception as e:
    print("Exception", e)
  return render_template('admin_top.html', users=users)


# 検索の処理
@admin_top.route('/admin/top', methods=['POST'])
def search():
  # ユーザ名取得
  user_name = json.loads(request.data)
  # ユーザ検索
  try:
    users = db.get_search_user(user_name)
  except Exception as e:
    return json.dumps({"data": []})
  return json.dumps({"data": users})


# ユーザ削除用
@admin_top.route('/admin/delete/<param>', methods=['GET'])
def user_delete(param):
  if param is None:
    return redirect('/admin/top')
  user_id = param
  try:
    db.delete_user(user_id)
  except Exception as e:
    print("Exception", e)
  return redirect('/admin/top')
