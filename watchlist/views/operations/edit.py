from flask import redirect, url_for, request, render_template
from watchlist import app
from flask_login import login_required, current_user
from watchlist.models import Stock

# ...

# 打开编辑
@app.route('/stock/edit', methods=['POST'])
@login_required 
def edit():
    stockcode = request.form['stockcode']
    stocks = Stock.query.filter_by(username=current_user.username, stockcode=stockcode).all()
    stock = None
    if len(stocks) > 0:
        stock = stocks[0]

    return render_template('edit.html', stock=stock)