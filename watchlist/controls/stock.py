import re
from flask import flash
from watchlist import req

# ...

# 个股信息
class StockInfo():
    def __init__(self):
        self.stockcode = ''
        self.stockname = ''
        self.pricenow = 0.0
        self.priceyesterday = 0.0

# 东方财富的请求地址中, 变化的一个数字, 有时候是0, 有时候是1, 不知道规律, 先尝试这两个值
class SecureId():
    secureid = 0
    @classmethod
    def getNewSecureId(cls):
        cls.secureid = 0 if cls.secureid == 1 else 1
        return cls.secureid

# 获取个股信息
def get_stock_info(stockcode):
    stockinfo = None
    try:
        # 通过股票代码获取个股信息
        stockname = getStockName(stockcode)
        if stockname is not None:
            prices = getStockPrices(stockcode)
            if prices is not None:
                stockinfo_temp = StockInfo()
                stockinfo_temp.stockname = stockname
                stockinfo_temp.stockcode = stockcode
                stockinfo_temp.pricenow = prices[0]
                stockinfo_temp.priceyesterday = prices[1]
                stockinfo = stockinfo_temp
            
    except BaseException as e:
        #flash(f"获取个股信息异常 --> {e}")
        pass

    return stockinfo

# ----------- 爬取 -----------
# 获取个股名称
def getStockName(stockcode):
    result = None
    try:
        url = "https://datacenter-web.eastmoney.com/web/api/data/v1/get?callback=jQuery35109920430474348196_1721061192365&reportName=RPTA_WEB_HQDAYS_NEW&columns=SCODE%2CSNAME%2CDAYS%2CHQCODE&filter=(SCODE%3D%22{0}%22)&token=28dfeb41d35cc81d84b4664d7c23c49f&source=WEB&client=WEB&_=1721061192379".format(stockcode)       
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',}
        response = req.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = "utf-8"
        data = re.compile(r'\[([^\]]+)\]').findall(response.text)[0]
        dataDict = eval(data.replace('"data":', ''))

        if stockcode == dataDict['SCODE']:
            result = dataDict['SNAME']
    except BaseException as e:
        #flash(f"获取个股名称异常 --> {e}")
        pass
    
    return result

# 通过最近的5个分钟K, 获取个股当前价格和前日收盘价格
def getStockPrices(stockcode):
    result = None

    try:
        result = getStockPricesWithSecureid(stockcode=stockcode, secureid=SecureId.secureid)
        if result is None:
            result = getStockPricesWithSecureid(stockcode=stockcode, secureid=SecureId.getNewSecureId())
    except BaseException as e:
        #flash(f"获取个股价格信息异常 --> {e}")
        pass

    return result

# 获取个股当前价格和前日收盘价格, 填充 secure id 
def getStockPricesWithSecureid(stockcode, secureid):
    result = None

    try:
        url = "http://push2.eastmoney.com/api/qt/stock/details/get?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55&fltt=2&cb=jQuery351016389108986805678_1721052534470&pos=-11&secid={0}.{1}&ut=fa5fd1943c7b386f172d6893dbfba10b&wbp2u=%7C0%7C0%7C0%7Cweb&_=1721052534471".format(secureid, stockcode)   
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',}
        response = req.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = "utf-8"
        data = re.compile(r'"data":{.*?}').findall(response.text)[0]
        dataDict =  eval(data.replace('"data":', ''))
        if stockcode == dataDict['code']:
            stockPrice = dataDict['details'][-1].split(',')[1]
            stockPrePrice = dataDict['prePrice']
            result = (stockPrice, stockPrePrice)
    except BaseException as e:
        pass

    return result