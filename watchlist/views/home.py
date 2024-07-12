from flask import render_template
from watchlist import app

# ...

# 主页
@app.route('/')
def home():
    return render_template('home.html')