from watchlist.controls.mail import send_inform_mail
from watchlist.controls.common import get_users, getTimeNow
from watchlist.models import Stock
from watchlist import app, db

# ...

# 当前天类
class ResetTrigger():
    day = getTimeNow().day

    # 天的数值变化则可以重置
    @classmethod
    def isTimeToReset(cls):
        result = False

        # 每天北京时间9:29到15:01任务执行 周六日除外
        newday = getTimeNow().day
        if newday != cls.day:
            cls.day = newday
            result = True

        return result

# 发送提醒邮件的任务, 定时执行
def sendinformEmails():
    try:
        flag_commit = False
        with app.app_context():
            for user in get_users():               
                stocks = []
                for stock in Stock.query.filter_by(username=user.username):
                    stocks.append(stock)
                flag_commit = flag_commit or send_inform_mail(user=user, stocks=stocks) 

            if flag_commit:
                db.session.commit()

            if ResetTrigger.isTimeToReset():
                for stock in Stock.query.all():
                    stock.resetinformedflags()
                db.session.commit() 
    except BaseException as e:
            pass    

