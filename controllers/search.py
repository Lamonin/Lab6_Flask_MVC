from flask import render_template, request, redirect, url_for, session
from models.search_model import get_genre_with_count, get_author_with_count, get_publisher_with_count, \
    get_filtered_books
from utils import get_db_connection
from app import app


def join_filter_list(df, selected):
    filter_list = []

    for i in range(len(df)):
        if df.iloc[i, 0] in selected:
            filter_list.append(df.iloc[i, 1])

    if len(filter_list) == 0:
        filter_list.append('-')

    return ', '.join(filter_list) + '.'


@app.route('/search', methods=['get', 'post'])
def search():
    conn = get_db_connection()

    selected_genres = request.values.getlist('genre_filter')
    selected_authors = request.values.getlist('author_filter')
    selected_publishers = request.values.getlist('publisher_filter')

    if request.method == 'POST':
        if 'back' in request.form:
            return redirect(url_for('index'))
        elif 'clear' in request.form:
            selected_genres = selected_authors = selected_publishers = []
        elif 'borrow_book' in request.form:
            session['borrow_book_id'] = request.values.get('borrow_book_id')
            return redirect(url_for('index'))

    genres = get_genre_with_count(conn)
    authors = get_author_with_count(conn)
    publishers = get_publisher_with_count(conn)

    filtered_books = get_filtered_books(
        conn,
        selected_genres,
        selected_authors,
        selected_publishers
    )

    return render_template(
        'search.html',
        filtered_books=filtered_books,
        genres=genres,
        authors=authors,
        publishers=publishers,
        selected_genres=[int(sg) for sg in selected_genres],
        selected_authors=[int(sa) for sa in selected_authors],
        selected_publishers=[int(sp) for sp in selected_publishers],
        len=len,
        join_filter_list=join_filter_list
    )
