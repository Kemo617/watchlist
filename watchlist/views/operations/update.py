from flask import redirect, url_for, request, flash
from watchlist import app
from watchlist.database import db
from watchlist.models import Stock
from flask_login import login_required, current_user

# ...

# 更新记录
@app.route('/stock/update', methods=['POST'])
@login_required 
def update():
    try:
        priceminset = float(request.form['priceminset'])
        pricemaxset = float(request.form['pricemaxset'])
        flag_is_informing = bool(request.form.get('setinform'))
        stockcode = request.form['stockcode']

        stocks = Stock.query.filter_by(username=current_user.username, stockcode=stockcode).all()

        for stock in stocks: 
            stock.priceminset = 0.0 if priceminset < 0 else priceminset
            stock.pricemaxset = 0.0 if pricemaxset < 0 else pricemaxset
            stock.flag_is_informing = flag_is_informing
            db.session.commit()
            flash('更新了对自选股票的邮件提醒设置.')
    except BaseException as e:
                flash(f"个股设置异常 --> {e}")

    
    return redirect(url_for('home'))