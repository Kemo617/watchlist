import efinance as ef
from flask import flash

# ...

# 个股信息
class StockInfo():
    def __init__(self):
        self.stockcode = ''
        self.stockname = ''
        self.pricenow = 0.0
        self.priceyesterday = 0.0

# 获取个股信息
def get_stock_info(stockcode):
    stockinfo = None
    try:
        # 通过股票代码获取个股信息
        lastdeal = ef.stock.get_deal_detail(stockcode).tail(1)
        linelabel = lastdeal.index.start
        if stockcode == lastdeal.loc[linelabel, '股票代码']:
            stockinfo = StockInfo()
            stockinfo.stockcode = lastdeal.loc[linelabel, '股票代码']
            stockinfo.stockname = lastdeal.loc[linelabel, '股票名称']
            stockinfo.pricenow = lastdeal.loc[linelabel, '成交价']
            stockinfo.priceyesterday = lastdeal.loc[linelabel, '昨收']
    except BaseException as e:
        flash(f"获取股票信息异常 --> {e}")

    return stockinfo