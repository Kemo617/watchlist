import click
from watchlist import app, db
from watchlist.models import User, SMTP
from sqlalchemy import text

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
@click.option('--sendername', prompt=True, help="The sender's name.")
@click.option('--senderaddress', prompt=True, help="The sender's email account.")
@click.option('--password', prompt=True, help="The password used to send emails.")
def setsmtp(server, sendername, senderaddress, password):
    db.create_all()

    smtp = SMTP.query.first()
    if smtp is not None:
        click.echo('Updating smtp infos ...')
    else:
        click.echo('Creating smtp infos ...')
        smtp = SMTP()
        db.session.add(smtp)

    smtp.server = server
    smtp.sendername = sendername
    smtp.senderaddress = senderaddress
    smtp.password = password

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
        user.username = username
        user.email = email
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')

# 激活用户
@app.cli.command()
@click.option('--username', prompt=True, help="Activate user.")
def activateuser(username):
    db.create_all()

    user = User.query.filter_by(username=username).first()
    if user is not None:
        if user.is_activated:
            click.echo('User %s already activated.' % username)
        else:
            click.echo('Activating user %s ...' % username)
            user.is_activated = True
            db.session.commit()
            click.echo('Done')
    else:
        click.echo('User not existed.')

# 设置用户为未激活
@app.cli.command()
@click.option('--username', prompt=True, help="Deactivate user.")
def deactivateuser(username):
    db.create_all()

    user = User.query.filter_by(username=username).first()
    if user is not None:
        if user.is_activated:
            click.echo('Deactivating user %s ...' % username)
            user.is_activated = False
            user.renewregistertime()
            db.session.commit()
            click.echo('Done')      
        else:
            user.renewregistertime()
            click.echo('User %s already deactivated.' % username)
    else:
        click.echo('User not existed.')

# 打印用户
@app.cli.command()
def listusers():
    db.create_all()

    for user in User.query.all():
        print(user.username)
    
# 删除用户
@app.cli.command()
@click.option('--username', prompt=True, help="Delete user.")
def deleteuser(username):
    db.create_all()

    user = User.query.filter_by(username=username).first()
    if user is not None:
        click.echo('Deleting user %s ...' % username)
        db.session.delete(user)
        db.session.commit()
        click.echo('Done')
    else:
        click.echo('User not existed.')
        
# 删除用户表
@app.cli.command()
def deleteusertable():
    db.create_all()
    db.session.execute(text("DROP TABLE IF EXISTS users"))
    click.echo('Done')
    db.create_all()

# 清理数据库
@app.cli.command()
def cleandb():
    db.create_all()
    # 清理删除用户后, 在个股表的残留
    click.echo('Done.')