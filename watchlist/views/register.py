from flask import render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, EqualTo, Length, Email
from watchlist import app
from watchlist.models import User
from flask_login import login_required, login_user, logout_user

# ...

# 定义表单模型类
class RegisterForm(FlaskForm):
    # DataRequired 验证不为空, Length 限制长度
    username = StringField(label=u"用户名", validators=[DataRequired(), Length(min=4, max=18)])
    password = PasswordField(label=u"密码", validators=[DataRequired(), Length(min=6, max=18)])
    repeat_password = PasswordField(label=u"再输一次", validators=[DataRequired(), EqualTo("password", u"两次密码输入不一致.")])
    email = EmailField(label=u"邮箱", validators=[DataRequired(), Email(u"请输入正确的邮箱地址.")])
    register = SubmitField(label=u"提交")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            repeat_password = form.password.data
            email = form.email.data
            flash(username + repeat_password + email)
        else:
            tips = ''
            for msg in form.repeat_password.errors:
                tips = msg
            for msg in form.email.errors:
                tips = msg
            if tips == '':
                tips = 'Please check Inputs.'
            flash(tips)
            
    return render_template('register.html', form=form)