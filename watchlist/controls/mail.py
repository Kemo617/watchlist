import smtplib
from email.message import EmailMessage
from watchlist.models import SMTP
from flask import render_template, flash

# ...

# 发送注册确认邮件
def send_confirm_mail(user):
    result = False
    smtpinfo = SMTP.query.first()

    sendInterval = user.time2sendconfirm()
    if sendInterval > 0:
        flash(u"请检查您邮箱中的注册确认信息. 如未收到, %s秒后可以重新发送邮件." % sendInterval)
    elif sendInterval < 0:
        if smtpinfo is not None:
            servername = smtpinfo.server
            sendername = smtpinfo.sendername
            senderaddress = smtpinfo.senderaddress
            password = smtpinfo.password
            html_content = render_template('confirm_email.html', user=user)

            message = EmailMessage()
            message['From'] = "%s<%s>" % (sendername, senderaddress)
            message['To'] = "%s<%s>" % (user.username, user.email)
            message['Subject'] = '注册确认'
            message.set_content(html_content, subtype='html')
            try:
                with smtplib.SMTP(servername) as server:
                    server.ehlo()
                    server.starttls()
                    server.login(senderaddress, password)
                    server.send_message(message)
                    user.renewregistertime()
                    user.addresendtimes()
                    result = True
            except BaseException as e:
                flash("发送异常-->{e}")
    else:
        flash(u"已经发了三次注册确认邮件. 换个可用的邮箱重新注册吧.")
    
    return result



# 发送定制的个股信息