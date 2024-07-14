from flask import redirect, url_for, request, flash
from watchlist import app, db
from flask_login import login_required, current_user
from watchlist.controls.stock import get_stock_info
from watchlist.controls.common import get_stockcodes
from watchlist.models import Stock

# ...

# 增加记录
@app.route('/stock/add', methods=['POST'])
@login_required 
def add():
    stockcode = request.form.get('stockcode')
    if not stockcode or len(stockcode) > 6:
        # 显示错误提示
        flash('股票代码输入错误.')
    else:
        # 判断是否已经添加过了
        stockcodes = get_stockcodes(current_user.username)
        if len(stockcodes) > 4:
            flash('已经加选了5支股票.')
        elif stockcode in stockcodes:
            flash('这支股已经添加过了.')
        else:
            stockinfo = get_stock_info(stockcode=stockcode)
            if stockinfo is not None:
                # 创建个股
                stock = Stock()
                stock.stockcode = stockinfo.stockcode
                stock.stockname = stockinfo.stockname
                stock.pricenow = stockinfo.pricenow
                stock.priceyesterday = stockinfo.priceyesterday
                stock.username = current_user.username

                db.session.add(stock)
                db.session.commit()
                flash('增加了一支自选股.')

    return redirect(url_for('home'))

