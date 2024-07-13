
from watchlist import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# ...

class SMTP(db.Model):
    __tablename__ = "smtp"
    id = db.Column(db.Integer, primary_key=True)
    server = db.Column(db.String(128))
    sender = db.Column(db.String(128))
    password = db.Column(db.String(128))
    

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128))
    register_time = db.Column(db.DateTime)
    is_activated = db.Column(db.Boolean)

    # 设置口令
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证口令
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class Movie(db.Model):
    __tablename__ = "stocks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))