from flask import render_template, request, redirect, url_for, session

from app import app


@app.route('/new_reader', methods=['get', 'post'])
def new_reader():
    if request.method == 'POST':
        if 'add_reader' in request.form:
            session['new_reader_name'] = request.values.get('new_reader_name')
            return redirect(url_for('index'))
        elif 'cancel' in request.form:
            return redirect(url_for('index'))

    return render_template('new_reader.html')
