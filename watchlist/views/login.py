from flask import render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from watchlist import app
from watchlist.models import User
from flask_login import login_required, login_user, logout_user

# ...

# 定义表单模型类
class LoginForm(FlaskForm):
    # DataRequired 验证不为空, Length 限制长度
    username = StringField(label=u"用户名", validators=[DataRequired(), Length(min=0, max=18)])
    password = PasswordField(label=u"密码", validators=[DataRequired(), Length(min=0, max=18)])
    submitlogin = SubmitField(label=u"登入")

# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            user = User.query.first()
            if username == user.username and user.validate_password(password):
                login_user(user)
                flash(u"已登入.")
                return redirect(url_for('home'))
            else:
                flash(u"错误的用户名或密码.")
        else:
            flash(u"无效输入.")

    return render_template('login.html', form=form)

# 登出
@app.route('/logout')
@login_required # 视图保护
def logout():
    logout_user()
    flash(u"已登出.")
    return redirect(url_for('home'))