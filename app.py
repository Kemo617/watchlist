import os
import sys
import click

from flask import Flask, url_for, request, redirect, flash, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
# 关闭对模型修改的监控
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 设置签名所需的密钥
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
# 初始化扩展,传入程序实例app
db = SQLAlchemy(app)
# 登陆管理类实例化
login_manager = LoginManager(app)
# 登录视图为起点
login_manager.login_view = 'showlogin'

# ----------------- 用户加载回调函数 -----------------
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

# ----------------- 数据模型 -----------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    ownername = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    # 设置口令
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证口令
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

# ----------------- 注册命令 -----------------------
# 初始化数据库
@app.cli.command() 
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

# 创建管理用户
@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def setadmin(username, password):
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user ...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user ...')
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')

# 设置所有者名
@app.cli.command()
@click.option('--ownername', prompt=True, help='The ownername of watchlist.')
def setowner(ownername):
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating owner ...')
        user.ownername = ownername
    else:
        click.echo('Creating owner ...')
        user = User(ownername=ownername)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')

# 向数据库填充电影示例数据
@app.cli.command()
def forgemovies():
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'}
    ]

    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

# --------------- 视图函数 -------------
# 主页
@app.route('/index')
def index():
    return render_template('index.html')

# 显示登录页面
@app.route('/login')
def showlogin():
    return render_template('login.html')

# 显示设置页面
@app.route('/settings')
def showsettings():
    return render_template('settings.html')

# 登入
@app.route('/loginA', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.first()
    if username == user.username and user.validate_password(password):
        login_user(user)
        flash('Login success.')
    else:
        flash('Invalid username or password.')
        return redirect(url_for('showlogin'))
        
    return redirect(url_for('index'))

# 登出
@app.route('/logout')
@login_required # 视图保护
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))

# 设置
@app.route('/settingsA', methods=['POST'])
@login_required 
def settings():
    ownername = request.form['ownername']
    if not ownername or len(ownername) > 20:
        flash('Invalid input.')
    else:
        current_user.ownername = ownername
        db.session.commit()
        flash('Settings updated.')

    return redirect(url_for('showsettings'))

# 增加记录
@app.route('/movie/add', methods=['POST'])
@login_required 
def add():
    title = request.form.get('title')
    year = request.form.get('year')
    if not title or not year or len(year) > 4 or len(title) > 60:
        # 显示错误提示
        flash('Invalid input.')
    else:
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')

    return redirect(url_for('index'))

# 打开编辑
@app.route('/movie/edit', methods=['POST'])
@login_required 
def edit():
    movie_id = request.form['movie_id']
    movie = Movie.query.get_or_404(movie_id)
    return render_template('edit.html', movie=movie)

# 更新记录
@app.route('/movie/update', methods=['POST'])
@login_required 
def update():
    title = request.form['title']
    year = request.form['year']
    movie_id = request.form['movie_id']

    if not title or not year or len(year) > 4 or len(title) > 60:
        # 显示错误提示
        flash('Invalid input.')
    else:
        # 更新表单数据
        movie = Movie.query.get_or_404(movie_id)
        movie.title =title
        movie.year = year
        db.session.commit()
        flash('Item updated.')

    return redirect(url_for('index'))

# 删除记录
@app.route('/movie/delete', methods=['POST'])
@login_required 
def delete():
    movie_id = request.form['movie_id']
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))

# --------------- 向模板注入 ----------
# 模板上下文处理函数, 注入用户信息
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

# 模板上下文处理函数, 注入电影信息
@app.context_processor
def inject_movies():
    movies = Movie.query.all()
    return dict(movies=movies)

# --------------- 错误页 -------------
# 404错误页
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# --------------- 测试 ---------------
@app.route('/hello')
def hello():
    imag_url = url_for('static', filename='images/halo.jpg')
    return '<h1>Hello Halo!</h1><img src=%s>' % imag_url

@app.route('/user/<name>')
def user_page(name):
    return '用户名: %s' % name

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='kemo'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num=2))
    return 'Test page'

if __name__ == '__main__':
    # 设置为调试模式
    app.run(debug=True)