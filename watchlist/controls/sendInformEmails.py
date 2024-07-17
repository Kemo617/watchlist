from watchlist.controls.mail import send_inform_mail
from watchlist.controls.common import get_users, getTimeNow
from watchlist.schedule import scheduler
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

# --------- 定时执行的任务 ------------
# 发送提醒邮件的任务
# 每20秒执行一次
@scheduler.task('interval', id='send_informemails_task', seconds=20)
def sendinformEmails():
    try:
        flag_commit = False

        for user in get_users():
            with app.app_context():
                stocks = []
                for stock in Stock.query.filter_by(username=user.username):
                    stocks.append(stock)
                flag_commit = flag_commit or send_inform_mail(user=user, stocks=stocks) 

        flag_commit = flag_commit or ResetTrigger.isTimeToReset()
        if flag_commit:
            for stock in Stock.query.all():
                stock.resetinformedflags()
            db.session.commit() 
    except BaseException as e:
            pass    

