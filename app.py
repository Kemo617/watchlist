from flask import Flask
from flask import url_for

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

@app.route('/user/<name>')
def user_page(name):
    return '用户名: %s' % name

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='kemo'))
    print(url_for('test_url_for'))
    return 'Test page'

if __name__ == '__main__':
    # 设置为调试模式
    app.run(debug=True)