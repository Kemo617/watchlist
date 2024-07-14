from flask import redirect, url_for
from watchlist import app
from flask_login import login_required

# ...

# 打开编辑
@app.route('/movie/edit', methods=['POST'])
@login_required 
def edit():
    '''
    movie_id = request.form['movie_id']
    movie = Movie.query.get_or_404(movie_id)
    return render_template('edit.html', movie=movie)
    '''
    return redirect(url_for('home'))