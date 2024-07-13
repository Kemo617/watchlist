
import uuid
from watchlist import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# ...

class SMTP(db.Model):
    __tablename__ = "smtp"
    id = db.Column(db.Integer, primary_key=True)
    server = db.Column(db.String(128))
    sendername = db.Column(db.String(20))
    senderaddress = db.Column(db.String(128))
    password = db.Column(db.String(128))
    

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128))
    register_time = db.Column(db.DateTime)
    is_activated = db.Column(db.Boolean)
    confirm_code = db.Column(db.String(128))
    resendtimes = db.Column(db.Integer)

    def __init__(self):
        # 注册时间, 即注册邮件发送时间
        self.register_time = datetime(1999, 9, 19, 9, 9, 9)
        # 随机字符串
        self.confirm_code = uuid.uuid4().hex
        self.resendtimes = 0

    # 设置口令
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证口令
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # 可以再次发送确认邮件的剩余时间, 0表示发送超过了3次
    def time2sendconfirm(self):
        now = datetime.now()
        time_difference = now - self.register_time
        # 5分钟后可以再次发送
        interval = 20 - round(time_difference.total_seconds())
        
        if self.resendtimes > 2:
            interval = 0

        return interval
    
    # 更新注册时间
    def renewregistertime(self):
        self.register_time = datetime.now()

    # 发送次数加1
    def addresendtimes(self):
        self.resendtimes += 1
        
class Movie(db.Model):
    __tablename__ = "stocks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))