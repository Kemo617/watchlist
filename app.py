import os
import sys
import click

from flask import Flask, url_for, request, redirect, flash, render_template
from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
# 关闭对模型修改的监控
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 设置签名所需的密钥
app.config['SECRET_KEY'] = 'dev'
# 初始户扩展,传入程序实例app
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

# 注册为命令, 初始化数据库
@app.cli.command() 
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

# 注册为命令, 向数据库填充示例数据
@app.cli.command()
def forge():
    db.create_all()

    name = 'Kemo'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'}
    ]

    user = User(name=name)
    db.session.add(user)
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

# 增加记录
@app.route('/movie/add', methods=['POST'])
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
def edit():
    movie_id = request.form['movie_id']
    movie = Movie.query.get_or_404(movie_id)
    return render_template('edit.html', movie=movie)

# 更新记录
@app.route('/movie/update', methods=['POST'])
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