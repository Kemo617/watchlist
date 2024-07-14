from flask import redirect, url_for, request, flash
from watchlist import app
from flask_login import login_required
from watchlist.controls.stock import get_stock_info

# ...

# 增加记录
@app.route('/movie/add', methods=['POST'])
@login_required 
def add():
    stockcode = request.form.get('stockcode')
    if not stockcode or len(stockcode) > 6:
        # 显示错误提示
        flash('股票代码输入错误.')
    else:
        stockinfo = get_stock_info(stockcode=stockcode)
        if stockinfo is not None:
            pass

        # 保存表单数据到数据库
        '''
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        '''

    return redirect(url_for('home'))