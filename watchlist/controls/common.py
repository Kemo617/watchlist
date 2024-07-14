from watchlist import db
from watchlist.models import Stock

# ...

# 得到某用户所有的个股代码
def get_stockcodes(username):
    stockcodes = []
    for stock in Stock.query.filter_by(username=username):
        stockcodes.append(stock.stockcode)
    return stockcodes