
from flask import jsonify
from watchlist import app
from watchlist.models import Stock
from flask_login import login_required, current_user

# ...

# 响应页面的刷新请求
@app.route('/refresh_pagedata')
@login_required 
def refresh_data():
    # 这里可以放置获取数据的逻辑
    data = {}
    for stock in Stock.query.filter_by(username=current_user.username):    
        data['#'+stock.stockcode] = (stock.pricenow, stock.getcolorclass())
    return jsonify(data)