import click
from watchlist import app, db
from watchlist.models import User, Movie

# ...

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
