from flask import redirect, url_for
from watchlist import app
from flask_login import login_required

# ...

# 更新记录
@app.route('/movie/update', methods=['POST'])
@login_required 
def update():
    '''
    title = request.form['title']
    year = request.form['year']
    movie_id = request.form['movie_id']

    if not title or not year or len(year) > 4 or len(title) > 60:
        # 显示错误提示
        flash('Invalid input.')
    else:
        # 更新表单数据
        movie = Movie.query.get_or_404(movie_id)
        movie.title =title
        movie.year = year
        db.session.commit()
        flash('Item updated.')

    '''
    return redirect(url_for('home'))