from flask import render_template
from watchlist import app

# ...

@app.route('/register')
def showregister():
    return render_template('register.html')