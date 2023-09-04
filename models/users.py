from app import db


class Users(db.Model):
  __tablename__ = 'Users'
  id = db.Column(db.Integer, primary_key=True)
  mail = db.Column(db.String(256), unique=True, nullable=False)
  hashed_password = db.Column(db.String(256), nullable=False)
  salt = db.Column(db.String(256), nullable=False)
  username = db.Column(db.String(256), nullable=False)
  rank_rate = db.Column(db.Integer, default=0)
  point = db.Column(db.Integer, default=0)

  def __init__(self, mail, hashed_password, salt, username, rank_rate=0, point=0):
    self.mail = mail
    self.hashed_password = hashed_password
    self.salt = salt
    self.username = username
    self.rank_rate = rank_rate
    self.point = point
