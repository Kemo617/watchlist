from flask import render_template, request, flash, redirect, url_for
from watchlist import app
from watchlist.models import User
from flask_login import login_required, login_user, logout_user

# 显示登录页面
@app.route('/login')
def showlogin():
    return render_template('login.html')

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
        
    return redirect(url_for('home'))

# 登出
@app.route('/logout')
@login_required # 视图保护
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('home'))