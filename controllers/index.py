from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.index_model import get_reader, get_book_reader, get_new_reader, borrow_book, return_book


@app.route('/', methods=['get'])
def index():
    conn = get_db_connection()

    if session.get('borrow_book_id', None):
        borrow_book(conn, session.pop('borrow_book_id'), session['reader_id'])

    if session.get('new_reader_name', None):
        reader_id = get_new_reader(conn, session.pop('new_reader_name'))
        session['reader_id'] = reader_id
    elif request.values.get('reader'):
        reader_id = int(request.values.get('reader'))
        session['reader_id'] = reader_id
    elif request.values.get('return'):
        book_reader_id = int(request.values.get('return'))
        return_book(conn, book_reader_id)
    elif not session.get('reader_id', None):
        session['reader_id'] = 1

    df_reader = get_reader(conn)
    df_book_reader = get_book_reader(conn, session['reader_id'])

    html = render_template(
        'index.html',
        reader_id=session['reader_id'],
        combo_box=df_reader,
        book_reader=df_book_reader,
        len=len
    )
    return html
