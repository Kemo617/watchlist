from flask import render_template
from watchlist import app
from flask_login import login_required

# ...

# 主页
@app.route('/')
@login_required 
def home():
    return render_template('home.html')