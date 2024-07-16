from watchlist import app
from watchlist.database import db
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from flask_login import current_user

# ...

# 显示设置页面
@app.route('/settings')
def showsettings():
    return render_template('settings.html')

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