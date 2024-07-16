from watchlist import socketio, app

# ...

if __name__ == '__main__':
    # 设置为调试模式
    socketio.run(app)