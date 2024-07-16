import os
import sys
import requests as req

from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
from watchlist.database import db
from watchlist.schedule import scheduler

# ...

app = Flask(__name__)

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
# sqlite数据库路径
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
# 关闭对模型修改的监控
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# session 存储所需的密钥
app.config['SECRET_KEY'] = 'kinson'

db.init_app(app)
login_manager = LoginManager(app)

# 用户加载回调函数
@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user

# 登录视图为起点
login_manager.login_view = 'login'
login_manager.login_message = ''

# 初始化定时任务
scheduler.init_app(app)
scheduler.start()

# 初始化socketio
socketio = SocketIO(app)

# 模板上下文处理函数, 注入用户信息
@app.context_processor
def inject_user():
    from flask_login import current_user
    return dict(user=current_user)

# 模板上下文处理函数, 注入电影信息
@app.context_processor
def inject_stocks():
    from watchlist.models import Stock
    from flask_login import current_user
    stocks = []
    
    try:
        stocks = Stock.query.filter_by(username=current_user.username).all()
    except:
        pass

    return dict(stocks=stocks)

from watchlist import test, commands, database, schedule
from watchlist.views import errors, home, login, register, settings
from watchlist.views.operations import add, delete, edit, update
from watchlist.controls import mail, stock, common, sendInformEmails, updateStockInfoTask, freshPage