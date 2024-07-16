from flask import redirect, url_for, request, flash
from watchlist import app
from watchlist.database import db
from flask_login import login_required, current_user
from watchlist.models import Stock

# ...

# 删除记录
@app.route('/stock/delete', methods=['POST'])
@login_required 
def delete():
    stockcode = request.form['stockcode']
    stocks = Stock.query.filter_by(username=current_user.username, stockcode=stockcode).all()

    for stock in stocks: 
        db.session.delete(stock)
        db.session.commit()
        flash('删除了一支自选股票.')

    return redirect(url_for('home'))