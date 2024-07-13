import click
from watchlist import app, db
from watchlist.models import User, SMTP
from datetime import datetime

# ...

# 初始化数据库
@app.cli.command() 
# @click.option('--drop', is_flag=True, help='Create after drop.')
def initdb():
    db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

# 设置smtp信息
@app.cli.command()
@click.option('--server', prompt=True, help="The smtp server used to send emails.")
@click.option('--sender', prompt=True, help="The sender's email account.")
@click.option('--password', prompt=True, help="The password used to send emails.")
def setsmtp(server, sender, password):
    db.create_all()

    smtp = SMTP.query.first()
    if smtp is not None:
        click.echo('Updating smtp infos ...')
        smtp.server = server
        smtp.sender = sender
        smtp.password = password
    else:
        click.echo('Creating smtp infos ...')
        smtp = SMTP()
        smtp.server = server
        smtp.sender = sender
        smtp.password = password
        db.session.add(smtp)

    db.session.commit()
    click.echo('Done.')

# 创建用户
@app.cli.command()
@click.option('--username', prompt=True, help="The username used to login.")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help="The password used to login.")
@click.option('--email', prompt=True, help="The user's email address.")
def setuser(username, password, email):
    db.create_all()

    user = User.query.filter_by(email=email).first()
    if user is not None:
        click.echo('Updating user ...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user ...')
        user = User()
        user.email = email
        user.username = username
        user.set_password(password)
        user.register_time = datetime.now()
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')

# 激活用户
@app.cli.command()
@click.option('--email', prompt=True, help="Activate user by email.")
def activate(email):
    db.create_all()

    user = User.query.filter_by(email=email).first()
    if user is not None:
        if user.is_activated:
            click.echo('User %s already activated.' % user.username)
        else:
            click.echo('Activating user %s ...' % user.username)
            user.is_activated = True
            db.session.commit()
            click.echo('Done')
    else:
        click.echo('User not existed.')