from flask import redirect, url_for
from watchlist import app
from flask_login import login_required

# ...

# 删除记录
@app.route('/movie/delete', methods=['POST'])
@login_required 
def delete():
    '''
    movie_id = request.form['movie_id']
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    '''
    return redirect(url_for('home'))