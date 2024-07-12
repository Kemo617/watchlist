from flask import render_template, request, flash, redirect, url_for
from watchlist import app, db
from watchlist.models import Movie
from flask_login import login_required

# ...

# 增加记录
@app.route('/movie/add', methods=['POST'])
@login_required 
def add():
    title = request.form.get('title')
    year = request.form.get('year')
    if not title or not year or len(year) > 4 or len(title) > 60:
        # 显示错误提示
        flash('Invalid input.')
    else:
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')

    return redirect(url_for('home'))

# 打开编辑
@app.route('/movie/edit', methods=['POST'])
@login_required 
def edit():
    movie_id = request.form['movie_id']
    movie = Movie.query.get_or_404(movie_id)
    return render_template('edit.html', movie=movie)

# 更新记录
@app.route('/movie/update', methods=['POST'])
@login_required 
def update():
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

    return redirect(url_for('home'))

# 删除记录
@app.route('/movie/delete', methods=['POST'])
@login_required 
def delete():
    movie_id = request.form['movie_id']
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('home'))