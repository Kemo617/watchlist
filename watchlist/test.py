from flask import url_for
from watchlist import app

# ...

@app.route('/hello')
def hello():
    imag_url = url_for('static', filename='images/halo.jpg')
    return '<h1>Hello Halo!</h1><img src=%s>' % imag_url

@app.route('/user/<name>')
def user_page(name):
    return '用户名: %s' % name

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='kemo'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num=2))
    return 'Test page'