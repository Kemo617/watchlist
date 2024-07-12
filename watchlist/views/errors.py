from watchlist import app
from flask import render_template
from flask_login import login_required

# ...

# 404错误页
@app.errorhandler(404)
@login_required 
def page_not_found(e):
    return render_template('404.html'), 404