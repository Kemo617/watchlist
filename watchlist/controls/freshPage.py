import time
from watchlist.controls.common import getTimeNow, is_need_refresh, reset_refresh

# ...
'''    
# --------- 刷新页面 ------------
# 刷新页面
@socketio.on('refresh_page_task')
def refreshpage():
    socketio.emit('refresh')

    while True:
        try:
            if is_need_refresh():
                reset_refresh()
                print('send fresh command')
        except BaseException as e:
            pass
    time.sleep(20)

'''